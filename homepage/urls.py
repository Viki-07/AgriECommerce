from django.urls import path
from . import views
from .payment import create_order, payment_callback

urlpatterns = [
    path('', views.home, name='home'),
    path('', views.home, name='products'),
    path('', views.home, name='farmers'),
    path('', views.home, name='about'),
    path('', views.home, name='contact'),
    path('', views.home, name='cart'),
    path('', views.home, name='category'),
    path('shop/', views.shop, name='shop'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path("add-to-cart/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/", views.cart_view, name="cart"),
    path("cart/remove/<int:item_id>/", views.remove_from_cart, name="remove_from_cart"),
    path('update_cart/<int:item_id>/<str:change>/', views.update_cart, name='update_cart'),

    path('category/<str:category_name>/', views.category_page, name='category_page'),
    path('orders/', views.orders_view, name='orders'),
    path('create-order/', create_order, name='create_order'),
    path('payment-callback/', payment_callback, name='payment_callback'),
    path('direct-checkout/', views.direct_checkout, name='direct_checkout'),
    path('order-success/<int:order_id>/', views.order_success, name='order_success'),
]
