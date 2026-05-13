from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.db import connection
from .models import Post

def home(request):
    posts = Post.objects.all()
    return render(request, "home.html", {"posts": posts})

@csrf_exempt
def add_post(request):
    if request.method == "POST":
        content = request.POST.get("content")

        # ❌ SQL Injection vulnerability
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO main_post (content, owner_id) VALUES ('" + content + "', 1)")

        return redirect("/")
    return redirect("/")

def delete_post(request, post_id):
    # ❌ no ownership check
    post = Post.objects.get(id=post_id)
    post.delete()
    return redirect("/")
