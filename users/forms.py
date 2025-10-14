from django import forms
from .models import UserProfile, User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ("user",)

        widgets = {
            'bio': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 5,
                }
            ),
        }


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

        widgets = {
            'username': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'password1': forms.PasswordInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'password2': forms.PasswordInput(
                attrs={
                    'class': 'form-control',
                }
            )
        }

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]

        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={
        'placeholder': 'EMAIL ADDRESS',
        'class': 'form-control',
    }))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={
        'placeholder': 'PASSWORD',
    }))
