from django.shortcuts import render
from django.shortcuts import redirect, get_object_or_404
from .models import Product
from .models import Cart
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'homepage/index.html')


# Create your views here.
def shop(request):
    products = Product.objects.all()
    return render(request, 'homepage/base.html', {'products': products})

def search_results(request):
    query = request.GET.get('q', '')  # Get the search query from the GET request
    if query:
        # Filter products based on the search query
        products = Product.objects.filter(name__icontains=query)
    else:
        products = []  # No products to display if no query is provided

    return render(request, 'homepage/search_results.html', {'products': products, 'query': query})

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Assuming you have a Cart model, update it
    cart_item, created = Cart.objects.get_or_create(user=request.user, ref_product=product)
    cart_item.quantity += 1
    cart_item.save()
    return redirect("cart")  # Redirect to home or cart page
def cart_view(request):
    cart_items = Cart.objects.filter(user=request.user)  # Get only the logged-in user's cart items
    total_price = sum(item.total_price() for item in cart_items)  # Calculate total price

    return render(request, "homepage/cart.html", {"cart_items": cart_items, "total_price": total_price})


@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(Cart, id=item_id, user=request.user)
    cart_item.delete()
    return redirect("cart")




def category_page(request, category_name):
    products = Product.objects.filter(category=category_name)  # ✅ Use category directly
    return render(request, 'homepage/categorypage.html', {'products': products, 'category_name': category_name})
