from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('', views.home, name='products'),
    path('', views.home, name='farmers'),
    path('', views.home, name='about'),
    path('', views.home, name='contact'),
    path('', views.home, name='cart'),
    path('', views.home, name='category'),
]
