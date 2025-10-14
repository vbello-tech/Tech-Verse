"""
URL configuration for users app.
"""

from django.urls import path, reverse_lazy
from .views import (
    home,
    SignupView,
    LoginView,
    LogoutView,
    CompleteProfileView,
    UserProfileView,
)

from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetCompleteView,
)

app_name = "user"

urlpatterns = [
    path('', home, name="home"),
    path('signup/', SignupView.as_view(), name="signup"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('complete-profile/', CompleteProfileView.as_view(), name="complete_profile"),
    path('profile/', UserProfileView.as_view(), name="profile"),
]
