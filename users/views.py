# users/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm  # If you have custom forms
from django.contrib import messages


# Register view
# users/views.py


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)  # Don't forget to handle file uploads (e.g. profile_image)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login after successful registration
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})


# Login view

from django.contrib.auth.forms import AuthenticationForm  # Import the form

def login_view(request):
    form = AuthenticationForm()  # Create an empty authentication form

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)  # Populate form with POST data
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'users/login.html', {'form': form})  # Pass the form to template


# Profile view
def profile(request):
    return render(request, 'users/profile.html')
