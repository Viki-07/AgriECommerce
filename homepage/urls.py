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
    path('shop/', views.shop, name='shop'),
    path("add-to-cart/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/", views.cart_view, name="cart"),
    path("cart/remove/<int:item_id>/", views.remove_from_cart, name="remove_from_cart"),

    path('category/<str:category_name>/', views.category_page, name='category_page'),

]
