from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from .models import UserProfile, User
from .forms import NewUserForm, LoginForm, UserProfileForm
from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib import auth
from django.contrib.auth import authenticate, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib import messages


# Create your views here.

def home(request):
    return render(request, 'home.html')


# sign up
class SignupView(View):
    """
    Signup view
    """

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            messages.info(self.request, "You already have an account.")
            return redirect('/')
        else:
            context = {
                'form': NewUserForm(self.request.POST)
            }
            print(self.request.user)
            return render(self.request, 'users/signup.html', context)

    def post(self, *args, **kwargs):
        if self.request.method == 'POST':
            form = NewUserForm(self.request.POST)
            if form.is_valid():
                user = form.save()
                # subject = 'SignUp'
                # html_message = render_to_string('users/signupemail.html', {'context': user.username})
                # plain_message = strip_tags(html_message)
                # mail.send_mail(subject, plain_message, settings.EMAIL_HOST_USER, [user.email],
                #                html_message=html_message)
                return redirect('user:login')
        else:
            form = NewUserForm()


# login
class LoginView(View):
    """
    Login view
    """

    def get(self, *args, **kwargs):
        form = LoginForm()
        context = {
            'form': form,
        }
        return render(self.request, 'users/login.html', context)

    def post(self, *args, **kwargs):
        form = LoginForm(self.request.POST or None)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(self.request, email=email, password=password)
            if user:
                auth.login(self.request, user)
                messages.success(self.request, "Account login successful.")
                return redirect('/')
            elif not User.objects.filter(email=form.cleaned_data['email']).exists():
                messages.info(self.request, "You dont have an account. Kindly signup.")
                return redirect('user:signup')
            else:
                messages.info(self.request, "Email or password incorrect.")
                return redirect('user:login')
        else:
            return redirect('user:login')


class LogoutView(View, LoginRequiredMixin):
    """
    Logout view
    """

    def get(self, *args, **kwargs):
        auth.logout(self.request)
        messages.success(self.request, "Account logout successful.")
        return HttpResponseRedirect('/')


# create profile
class CompleteProfileView(View, LoginRequiredMixin):
    """
    Create password view
    """

    def get(self, *args, **kwargs):
        profile = get_object_or_404(UserProfile, user=self.request.user)
        form = UserProfileForm(self.request.POST, self.request.FILES, instance=profile)
        context = {
            'form': form,
        }
        return render(self.request, 'users/createprofile.html', context)

    def post(self, *args, **kwargs):
        profile = get_object_or_404(UserProfile, user=self.request.user)
        form = UserProfileForm(self.request.POST, self.request.FILES, instance=profile)
        if form.is_valid():
            bio = form.cleaned_data.get('bio')
            image = form.cleaned_data.get('image')
            stack = form.cleaned_data.get('stack')
            github = form.cleaned_data.get('github')
            twitter = form.cleaned_data.get('twitter')
            linkedin = form.cleaned_data.get('linkedin')
            other = form.cleaned_data.get('other')
            profile.bio = bio
            profile.image = image
            profile.stack = stack
            profile.github = github
            profile.twitter = twitter
            profile.linkedin = linkedin
            profile.other = other
            profile.save()
            return redirect(profile.get_profile())
        else:
            form = UserProfileForm()


class UserProfileView(View):
    """
    View user profile view
    """

    def get(self, request, *args, **kwargs):
        context = {
            'profile': UserProfile.objects.get(user=request.user),
        }
        return render(self.request, 'users/profile.html', context)
