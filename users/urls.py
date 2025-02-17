# users/urls.py

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Define your user-related URLs here, such as registration, login, etc.
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='users/logout.html'),name='logout'),
    path('profile/', views.profile, name='profile'),
]
