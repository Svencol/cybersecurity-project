from django.urls import path
from .views import home, add_post, delete_post, debug_info, ping, read_file

urlpatterns = [
    path("", home),
    path("add/", add_post),
    path("delete/<int:post_id>/", delete_post),
    path("debug/", debug_info),
    path("ping/", ping),
    path("read/", read_file),
]