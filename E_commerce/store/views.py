from django.shortcuts import render, get_object_or_404
from .models import OrderItem, Product
from .cart import Cart
from .models import Product
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .cart import Cart
from .models import Order, OrderItem
from .forms import CheckoutForm
import stripe
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .forms import CustomRegisterForm
from django.http import HttpResponse


def index(request):
    products = Product.objects.all()
    return render(request, 'index.html',{'products': products })

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'product_detail.html', {'product': product})

def add_to_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product=product)
    return redirect('cart_detail')

def remove_from_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart_detail')

def cart_detail(request):
 cart = Cart(request)
 return render(request, 'cart_detail.html',{'cart':cart})

def order_success(request):
    return render(request, 'order_success.html')

def increase_quantity(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    for item in cart:
        if item['product'].id == product.id:
            quantity = item['quantity'] + 1
            cart.update_quantity(product, quantity)
            break
    return redirect('cart_detail')

def decrease_quantity(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    for item in cart:
        if item['product'].id == product.id:
            quantity = item['quantity'] - 1
            cart.update_quantity(product, quantity)
            break
    return redirect('cart_detail')


def register(request):
    if request.method == 'POST':
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomRegisterForm()
    return render(request, 'register.html', {'form': form})


stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def create_checkout_session(request):
    cart = Cart(request)
    line_items = []

    for item in cart:
        line_items.append({
            'price_data': {
                'currency': 'inr',
                'product_data': {
                    'name': item['product'].name,
                },
                'unit_amount': int(item['price'] * 100),  # in paisa
            },
            'quantity': item['quantity'],
        })

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        success_url=request.build_absolute_uri('/order_success/'),
        cancel_url=request.build_absolute_uri('/cart/'),
    )

    return JsonResponse({'id': session.id})
       
@login_required
def profile_view(request):
    orders = Order.objects.filter(user=request.user).order_by('-created')
    return render(request, 'profile.html', {
        'user': request.user,
        'orders': orders
    })



@login_required
def checkout(request):
    cart = Cart(request)

    if len(cart.cart) == 0:
        return redirect('cart_detail')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(
                user=request.user if request.user.is_authenticated else None,
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                address=form.cleaned_data['address'],
                city=form.cleaned_data['city'],
                price=cart.get_total_price()
            )

            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )

            cart.clear()
            return redirect('order_success')  # Create this view or use a thank-you page

    else:
        form = CheckoutForm()

    return render(request, 'checkout.html', {
        'form': form,
        'cart': cart,
        'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLISHABLE_KEY,
    })
        
stripe.api_key = settings.STRIPE_SECRET_KEY

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    endpoint_secret = 'your_webhook_signing_secret'  # From Stripe dashboard
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        return HttpResponse(status=400)  # Invalid payload
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)  # Invalid signature

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        customer_email = session['customer_details']['email']
        total_amount = session['amount_total'] / 100

        # Update order (you may want to match it using metadata instead)
        # Optional: look up and mark the order as paid
        print("Payment was successful for:", customer_email)

    return HttpResponse(status=200)
           
            
             
    

    