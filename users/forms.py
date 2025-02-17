from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'profile_image')  # Add any fields you need

    # Remove or customize help text for password fields
    password1 = forms.CharField(
        widget=forms.PasswordInput,
        help_text=None  # Remove the help text
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput,
        help_text=None  # Remove the help text
    )
