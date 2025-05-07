# users/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm  # If you have custom forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from homepage.models import Cart, Order


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
@login_required
def profile(request):
    # Get user's orders
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    # Get user's cart items
    cart_items = Cart.objects.filter(user=request.user)
    
    return render(request, 'users/profile.html', {
        'orders': orders,
        'cart_items': cart_items
    })

@login_required
def edit_profile(request):
    if request.method == 'POST':
        # Update user information
        user = request.user
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        
        # Handle profile image upload if provided
        if 'profile_image' in request.FILES:
            user.profile_image = request.FILES['profile_image']
        
        user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')
    
    return render(request, 'users/edit_profile.html')
