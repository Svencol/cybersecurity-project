from django.shortcuts import render, redirect
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from .models import Post
import os

# 🔴 FLAW: A07 Identification and Authentication Failures
# No authentication required for any action


def home(request):
    posts = Post.objects.all()
    return render(request, "home.html", {"posts": posts})


# 🔴 FLAW: Information Disclosure (A05 / A02)
def debug_info(request):
    return render(request, "debug.html", {
        "settings": request.META
    })

    # ✅ FIX (commented):
    # return render(request, "debug.html", {})


# 🔴 FLAW 1: SQL Injection (A03)
# 🔴 FLAW 4: CSRF disabled
@csrf_exempt
def add_post(request):
    if request.method == "POST":
        content = request.POST.get("content")

        # ❌ Vulnerable SQL injection
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO main_post (content, owner_id) VALUES ('" + content + "', 1)"
            )

        # ✅ FIX (commented):
        # with connection.cursor() as cursor:
        #     cursor.execute(
        #         "INSERT INTO main_post (content, owner_id) VALUES (%s, %s)",
        #         [content, 1]
        #     )

    return redirect("/")


# 🔴 FLAW 3: Broken Access Control (A01)
def delete_post(request, post_id):

    # ❌ No ownership validation
    post = Post.objects.get(id=post_id)
    post.delete()

    # ✅ FIX (commented):
    # post = Post.objects.get(id=post_id, owner=request.user)
    # post.delete()

    return redirect("/")


# 🔴 FLAW: Command Injection (A03 additional coverage)
def ping(request):
    host = request.GET.get("host", "")

    # ❌ Vulnerable command execution
    result = os.popen("ping -n 1 " + host).read()

    return render(request, "ping.html", {"result": result})

    # ✅ FIX (commented):
    # import subprocess
    # result = subprocess.run(
    #     ["ping", "-n", "1", host],
    #     capture_output=True,
    #     text=True
    # ).stdout


# 🔴 FLAW: Path Traversal (A01/A05)
def read_file(request):
    filename = request.GET.get("file", "")

    # ❌ No validation of file path
    try:
        with open(filename, "r") as f:
            content = f.read()
    except:
        content = "Error reading file"

    return render(request, "file.html", {"content": content})

    # ✅ FIX (commented):
    # allow only safe directory access


# 🔴 FLAW: A09 Security Logging and Monitoring Failures
# No logging of important actions (create/delete)

# ✅ FIX (commented):
# import logging
# logger = logging.getLogger(__name__)
# logger.warning("Post deleted")