"""
URL configuration for blog app.
"""
from django.urls import path
from .views import (
    ShortListView,
)

app_name = "short"

urlpatterns = [
    path('', ShortListView.as_view(), name="list"),
]
