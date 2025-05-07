from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Order, OrderItem, Cart, Product
from django.contrib.auth.decorators import login_required

# Try to import razorpay, but don't fail if it's not available
try:
    import razorpay
    # Check if Razorpay keys are configured
    if settings.RAZORPAY_KEY_ID == 'your_razorpay_key_id' or settings.RAZORPAY_KEY_SECRET == 'your_razorpay_key_secret':
        RAZORPAY_AVAILABLE = False
        print("Warning: Razorpay API keys are not configured. Please update your settings.py file with your actual Razorpay API keys.")
    else:
        # Initialize Razorpay client
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        RAZORPAY_AVAILABLE = True
except ImportError:
    RAZORPAY_AVAILABLE = False
    print("Warning: Razorpay package not available. Payment functionality will be disabled.")
except Exception as e:
    RAZORPAY_AVAILABLE = False
    print(f"Warning: Error initializing Razorpay: {str(e)}")

def create_order(request):
    if not RAZORPAY_AVAILABLE:
        return JsonResponse({
            'error': 'Payment service not available. Please configure your Razorpay API keys in settings.py.',
            'details': 'To enable payments, sign up for a Razorpay account, get your API keys, and update your settings.py file.'
        }, status=503)
        
    try:
        data = json.loads(request.body)
        amount = data.get('amount')  # Amount in paise
        
        # Create Razorpay Order
        order_data = {
            'amount': amount,
            'currency': 'INR',
            'payment_capture': 1
        }
        order = client.order.create(data=order_data)
        
        return JsonResponse({
            'order_id': order['id'],
            'amount': order['amount'],
            'currency': order['currency']
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@login_required
def payment_callback(request):
    if not RAZORPAY_AVAILABLE:
        return JsonResponse({
            'error': 'Payment service not available. Please configure your Razorpay API keys in settings.py.',
            'details': 'To enable payments, sign up for a Razorpay account, get your API keys, and update your settings.py file.'
        }, status=503)
        
    try:
        # Verify payment signature
        params_dict = {
            'razorpay_payment_id': request.POST.get('razorpay_payment_id'),
            'razorpay_order_id': request.POST.get('razorpay_order_id'),
            'razorpay_signature': request.POST.get('razorpay_signature'),
        }
        
        client.utility.verify_payment_signature(params_dict)
        
        # Get the request data
        data = json.loads(request.body)
        product_id = data.get('product_id')
        quantity = data.get('quantity')
        
        if product_id and quantity:
            # Direct product purchase
            product = Product.objects.get(id=product_id)
            total_amount = product.price * quantity * 1.18  # Add 18% tax
            
            # Create a new order
            order = Order.objects.create(
                user=request.user,
                total_amount=total_amount,
                status='processing',
                shipping_address=request.user.profile.address if hasattr(request.user, 'profile') else ''
            )
            
            # Create order item
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=product.price
            )
        else:
            # Cart checkout
            cart_items = Cart.objects.filter(user=request.user)
            if not cart_items.exists():
                return JsonResponse({'error': 'No items in cart'}, status=400)
                
            # Create a new order
            order = Order.objects.create(
                user=request.user,
                total_amount=sum(item.total_price() for item in cart_items),
                status='processing',
                shipping_address=request.user.profile.address if hasattr(request.user, 'profile') else ''
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
        
        # Payment successful
        return JsonResponse({'status': 'success', 'order_id': order.id})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400) 