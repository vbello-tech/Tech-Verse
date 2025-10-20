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

    # PasswordResetView sends the mail
    path('reset-password/', PasswordResetView.as_view(
        template_name='accounts/password_reset.html',
        html_email_template_name='registration/password_reset_email.html',
        success_url=reverse_lazy('user:password_reset_done')
    ), name="password_reset"),
    path('password-reset-done/', PasswordResetDoneView.as_view(
        template_name='accounts/password_reset_done.html'),
        name="password_reset_done"),
    path('password-reset-confirm/(<uidb64>)-(<token>)/', PasswordResetConfirmView.as_view(
        template_name='accounts/password_reset_confirm.html',
        success_url=reverse_lazy('user:password_reset_complete')
    ),  name="password_reset_confirm"),
    path('password-reset-complete/', PasswordResetCompleteView.as_view(
        template_name='account/password_reset_complete.html'),
        name="password_reset_complete"),

]
