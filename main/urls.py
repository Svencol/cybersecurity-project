from django.urls import path
from .views import home, add_post

urlpatterns = [
    path('delete/<int:post_id>/', delete_post),
    path("", home),
    path("add/", add_post),
]
