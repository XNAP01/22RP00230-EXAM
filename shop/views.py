from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Order, OrderItem
from .forms import CheckoutForm, SignUpForm, LoginForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

def product_list(request):
    products = Product.objects.all()
    return render(request, 'shop/product_list.html', {'products': products})

def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session['cart'] = cart
    return redirect('product_list')

def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
    request.session['cart'] = cart
    return redirect('view_cart')

def view_cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0
    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, pk=product_id)
        subtotal = product.price * quantity
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal
        })
        total += subtotal
    return render(request, 'shop/cart.html', {'cart_items': cart_items, 'total': total})

@login_required(login_url='login')
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('view_cart')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(
                user=request.user if request.user.is_authenticated else None,
                full_name=form.cleaned_data['full_name'],
                address=form.cleaned_data['address'],
                payment_method=form.cleaned_data['payment_method'],
            )
            for product_id, quantity in cart.items():
                product = get_object_or_404(Product, id=product_id)
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price=product.price
                )
            request.session['cart'] = {}  # Clear cart after order
            return render(request, 'shop/order_success.html', {'order': order})
    else:
        form = CheckoutForm()

    return render(request, 'shop/checkout.html', {'form': form})

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-date_ordered')
    return render(request, 'shop/order_history.html', {'orders': orders})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('product_list')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def profile(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'shop/profile.html', {'orders': orders})

def products_by_category(request, category_name):
    products = Product.objects.filter(category=category_name)
    return render(request, 'shop/products_by_category.html', {'products': products, 'category': category_name})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('product_list')  # Already logged in

    form = LoginForm(request.POST or None)
    error = None

    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('product_list')
            else:
                error = 'Invalid username or password.'

    return render(request, 'shop/login.html', {'form': form, 'error': error})

def logout_view(request):
    logout(request)
    return redirect('login')  # or 'product_list'