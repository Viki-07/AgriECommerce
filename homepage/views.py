from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Cart, Order, OrderItem
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.conf import settings
from .recommender import ProductRecommender
from .sklearn_recommender import SklearnRecommender

# Initialize the sklearn recommender
sklearn_recommender = SklearnRecommender()

def home(request):
    return render(request, 'homepage/index.html')

def shop(request):
    products = Product.objects.all()
    cart_items = Cart.objects.filter(user=request.user) if request.user.is_authenticated else []
    
    # Get filter parameters
    category = request.GET.get('category')
    price_range = request.GET.get('price')
    sort_by = request.GET.get('sort')
    
    # Apply filters
    if category:
        products = products.filter(category=category)
    
    if price_range:
        if price_range == '0-500':
            products = products.filter(price__lte=500)
        elif price_range == '500-1000':
            products = products.filter(price__gt=500, price__lte=1000)
        elif price_range == '1000-5000':
            products = products.filter(price__gt=1000, price__lte=5000)
        elif price_range == '5000+':
            products = products.filter(price__gt=5000)
    
    # Apply sorting
    if sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
    elif sort_by == 'name':
        products = products.order_by('name')
    else:  # newest first (default)
        products = products.order_by('-created_at')
    
    # Get recommended products using ProductRecommender
    if request.user.is_authenticated:
        recommended_products = ProductRecommender.get_user_based_recommendations(request.user)
    else:
        recommended_products = ProductRecommender.get_popular_products()
    
    # Pagination
    paginator = Paginator(products, 12)  # Show 12 products per page
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    # If it's an AJAX request, return JSON response
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        products_data = [{
            'id': product.id,
            'name': product.name,
            'price': str(product.price),
            'category': product.category,
            'stock': product.stock,
            'image_url': product.image.url if product.image else None,
        } for product in page_obj]
        return JsonResponse({
            'products': products_data,
            'has_next': page_obj.has_next(),
            'has_previous': page_obj.has_previous(),
            'current_page': page_obj.number,
            'total_pages': paginator.num_pages
        })
    
    return render(request, 'homepage/shop.html', {
        'products': page_obj,
        'recommended_products': recommended_products,
        'cart_items': cart_items,
        'selected_category': category,
        'selected_price': price_range,
        'selected_sort': sort_by,
        'paginator': paginator,
        'page_obj': page_obj
    })

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_items = Cart.objects.filter(user=request.user) if request.user.is_authenticated else []
    razorpay_key_id = getattr(settings, 'RAZORPAY_KEY_ID', None)
    
    return render(request, 'homepage/product_detail.html', {
        'product': product,
        'cart_items': cart_items,
        'razorpay_key_id': razorpay_key_id
    })

def search_results(request):
    cart_items = Cart.objects.filter(user=request.user) if request.user.is_authenticated else []
    query = request.GET.get('q', '')
    products = Product.objects.filter(name__icontains=query) if query else []
    return render(request, 'homepage/search_results.html', {'products': products, 'query': query, "cart_items": cart_items})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))

    cart_item, created = Cart.objects.get_or_create(user=request.user, ref_product=product)

    if created:
        cart_item.quantity = quantity  # Set selected quantity if new
    else:
        cart_item.quantity = quantity  # Overwrite instead of adding

    cart_item.save()
    return redirect("cart")


def cart_view(request):
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        total_price = sum(item.total_price() for item in cart_items)
    else:
        cart_items = []
        total_price = 0
        
    # Check if Razorpay is configured
    razorpay_key_id = getattr(settings, 'RAZORPAY_KEY_ID', None)
    
    return render(request, "homepage/cart.html", {
        "cart_items": cart_items, 
        "total_price": total_price,
        "razorpay_key_id": razorpay_key_id
    })

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Cart

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Cart


from django import template

register = template.Library()

@register.filter
def mul(value, arg):
    """Multiplies the value by arg"""
    return round(value * arg, 2)

def update_cart(request, item_id, change):
    if request.method == "POST":
        cart_item = get_object_or_404(Cart, id=item_id, user=request.user)
        product = cart_item.ref_product  # Get the related product

        try:
            change = int(change)  # Convert string to integer
        except ValueError:
            return JsonResponse({"success": False, "error": "Invalid change value"}, status=400)

        # Calculate new quantity
        new_quantity = cart_item.quantity + change
        if new_quantity > product.stock:
            return JsonResponse({
                "success": False,
                "error": "Reached max stock limit",
                "new_quantity": cart_item.quantity
            })

        new_quantity = max(1, new_quantity)  # Prevent below 1
        cart_item.quantity = new_quantity
        cart_item.save()

        # Calculate total prices
        new_total_price = cart_item.quantity * product.price
        cart_total = sum(item.quantity * item.ref_product.price for item in Cart.objects.filter(user=request.user))

        return JsonResponse({
            "success": True,
            "new_quantity": cart_item.quantity,
            "new_total_price": new_total_price,
            "cart_total": cart_total
        })

    return JsonResponse({"success": False}, status=400)

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(Cart, id=item_id, user=request.user)
    cart_item.delete()
    return redirect("cart")

def category_page(request, category_name):
    cart_items = Cart.objects.filter(user=request.user) if request.user.is_authenticated else []
    products = Product.objects.filter(category=category_name)
    return render(request, 'homepage/categorypage.html', {'products': products, 'category_name': category_name, "cart_items": cart_items})

@login_required
def orders_view(request):
    """View to display user's order history"""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    cart_items = Cart.objects.filter(user=request.user) if request.user.is_authenticated else []
    
    return render(request, 'homepage/orders.html', {
        'orders': orders,
        'cart_items': cart_items
    })

@login_required
def direct_checkout(request):
    if request.method == 'POST':
        cart_items = Cart.objects.filter(user=request.user)
        if not cart_items.exists():
            return redirect('cart')
            
        # Create a new order
        order = Order.objects.create(
            user=request.user,
            total_amount=sum(item.total_price() for item in cart_items),
            status='Pending'
        )
        
        # Create order items and clear cart
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.ref_product,
                quantity=cart_item.quantity,
                price=cart_item.ref_product.price
            )
            cart_item.delete()
            
        return redirect('orders')
        
    return redirect('cart')

@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'homepage/order_success.html', {
        'order': order
    })
