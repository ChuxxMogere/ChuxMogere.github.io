import os
from lib2to3.fixes.fix_input import context

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, Cart, Order, OrderItem, Notification
from market.forms import RegisterForm, LoginForm, ProductForm, ProfileUpdateForm
from django.http import JsonResponse, HttpResponse
from django.core.mail import send_mail
from .models import Product
from .weather_service import get_weather_data, get_weather_forecast


# Create your views here.
def index(request):
    return render(request, 'index.html')

def register(request):
    message= None
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            message = 'Registered successfully '
            return redirect('login_view')
        else:
            message= 'Form is not valid'
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form, 'message': message})

def login_view(request):
    message = None
    form = LoginForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_buyer:
                login(request, user)
                return redirect('buyer_dashboard')
            elif user is not None and user.is_farmer:

                login(request, user)
                return redirect('farmer_dashboard')
            else:
                message = 'Invalid Credentials'
        else:
            message = 'Form is not valid'
    return render(request, 'login_view.html', {'form': form, 'message': message})

@login_required
def farmer_dashboard(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.farmer = request.user
            product.save()

            messages.success(request, 'Product uploaded successfully!')
            return redirect('farmer_dashboard')
    else:
        form = ProductForm()
    products = Product.objects.filter(farmer=request.user)
    context = {
        'form': form,
        'products': products,

    }
    return render(request, 'farmer_dashboard.html', context)

def weather_updates(request):
    city_name = request.GET.get("city_name", "Nairobi")
    current_weather = get_weather_data(city_name)
    weather_forecast = get_weather_forecast(city_name)

    context = {
        'current_weather': current_weather,
        'forecast': weather_forecast,
        'city_name': city_name,
    }
    return render(request, 'weather_updates.html', context)

@login_required
def delete_product(request,id):
    product = get_object_or_404(Product, id= id)
    try:
        product.delete()
        messages.success(request, f'Product deleted successfully!')
    except Exception as e:
        messages.error(request, f'Product not deleted')

    return redirect('farmer_dashboard')

@login_required
def buyer_dashboard(request, form=None):


    products = Product.objects.all()
    print(products)
    context = {
        'form': form,
        'products': products,
    }
    return render(request, 'buyer_dashboard.html', context)


def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    quantity = int(request.POST.get('quantity', 1)) if request.method == 'POST' else 1
    total_price = product.price * quantity

    if request.method == 'POST':
        cart_item, created = Cart.objects.get_or_create(product=product, user=request.user)
        cart_item.quantity += quantity
        cart_item.save()
        messages.success(request, f"{product.name} has been added to your cart!")

    context = {
        'product': product,
        'quantity': quantity,
        'total_price': total_price,
    }
    return render(request, 'product_detail.html', context)

def add_to_cart(request, id):
    product = get_object_or_404(Product, id=id)
    quantity = int(request.POST.get('quantity', 1))

    cart_item, created = Cart.objects.get_or_create(product=product, user=request.user)
    cart_item.quantity += quantity
    cart_item.save()

    messages.success(request, f"{product.name} has been added to your cart!")
    return redirect('product_detail', id=id)


def cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = int(sum(item.product.price * item.quantity for item in cart_items))

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'cart.html', context)

def update_cart_item(request, id):
    if request.method == 'POST':
        cart_item = get_object_or_404(Cart, id=id, user=request.user)
        operation = request.POST.get('operation')
        if operation == 'increase':
            cart_item.quantity += 1
        elif operation == 'decrease' and cart_item.quantity > 1:
            cart_item.quantity -= 1
        cart_item.save()
    return redirect('cart')

def remove_from_cart(request, cart_item_id):
    if request.method == "POST":
        cart_item = Cart.objects.get(id=cart_item_id, user=request.user)
        cart_item.delete()
        messages.success(request, "Item removed from cart")
        return redirect('cart')

def checkout(request, id=None, total_price=None, quantity=None):
    items = []
    farmer = None
    delivery_fee = 200

    cart_items = Cart.objects.filter(user=request.user)
    total_price = int(sum(item.product.price * item.quantity for item in cart_items))
    farmers = set(item.product.farmer for item in cart_items)
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'delivery_fee': delivery_fee,
    }
    return render(request, 'checkout.html', context)
def place_order(request):
    global message
    total_price = request.POST['total_price']
    cart_items = Cart.objects.filter(user=request.user)

    if not cart_items:
        messages.error(request, 'Your cart is empty.')
        return redirect('cart')

    delivery_option = request.POST['delivery_option']
    print("Delivery option: ", delivery_option)

    # Step 4: Create the order
    order = Order.objects.create(
        user=request.user,
        total_price=total_price,
        delivery_option=delivery_option,
    )
    order.save()

    # Create Order Items and send notifications
    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price,
        )

        # Notify the farmer
        farmer = item.product.farmer
        product_name = item.product.name
        buyer_email = request.user.email

        # Create a message for the farmer
        message = f"An order has been placed for {product_name}.\n"
        message += f"Buyer Details: Name: {request.user.username}, Email: {buyer_email}\n"
        message += f"Delivery Option: {delivery_option}, Quantity: {item.quantity}, Total Price: Ksh {total_price}"

        # Save notification to the database
        Notification.objects.create(
            farmer=farmer,
            message=message,
            order=order,
        )

        # Send an email to the farmer
        send_mail(
            'New Order Notification',
            message,
            settings.EMAIL_HOST_USER,
            [farmer.email],  # Farmer's email address
            fail_silently=False,
        )

    # Clear the cart
    cart_items.delete()

    return redirect('order_success')

def complete_order(request):

    global products, message
    total_price = request.POST['total_price']
    cart_items = Cart.objects.filter(user=request.user)
    if not cart_items:
        messages.error(request, 'Your cart is empty.')
        return redirect('cart')

    delivery_option = request.POST['delivery_option']
    print("Delivery option: ", delivery_option)

    # Step 4: Create the order
    order = Order.objects.create(
        user=request.user,
        total_price=total_price,
        delivery_option=delivery_option,
        # status='pending',
    )
    order.save()

    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price,
        )





    for item in cart_items:
        farmer = item.product.farmer
        products = [item.product.name for item in cart_items]
        message = f"An order has been placed for the following items: {', '.join(products)}"
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone = request.POST['phone']
        farm = 'cynthiamogere7@gmail.com'
        send_mail(
            'Billing Order',
            f"{message} ",
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,

        )
        return redirect('order_success')
    return redirect('cart')

def order_success(request):

    order = Order.objects.filter(user=request.user).latest('created_at')
    return render(request, 'order_success.html', {'order': order})

def logout_view(request):
    logout(request)
    return redirect('index')

@login_required
def profile_view(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=user)
    return render(request, 'profile.html', {'form': form})

def farmer_notifications(request):
    if not request.user.is_farmer:
        return redirect('home')  # Redirect if the user is not a farmer

    unread_notifications_count = Notification.objects.filter(farmer=request.user, is_read=False).count()
    context = {
        'unread_notifications_count': unread_notifications_count
    }

    return render(request, 'farmer_notifications.html', context)









