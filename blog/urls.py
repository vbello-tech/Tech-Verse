"""
URL configuration for blog app.
"""
from django.urls import path
from .views import (
    BlogListView,
    CreateBlogView,
    BlogDetailView,
)

app_name = "blog"

urlpatterns = [
    path('', BlogListView.as_view(), name="list"),
    path('create/', CreateBlogView.as_view(), name="create"),
    path('<str:slug>/', BlogDetailView.as_view(), name="detail"),
]
