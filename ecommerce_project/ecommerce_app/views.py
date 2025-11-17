from django.shortcuts import render,redirect,get_object_or_404
from .models import Customer
from .models import Product,Category,Cart,Wishlist
from django.contrib import messages

def base(request):
    return render(request,'base.html')

def home(request):
    categories = [
        {"name": "Mobile", "image": "images/mobiles.webp"},
        {"name": "Electronics", "image": "images/electronics.jpg"},
        {"name": "Fashion", "image": "images/fashion.webp"},
        {"name": "Books", "image": "images/books.jpg"},
        {"name": "Home", "image": "images/home.webp"},
        {"name": "Grocery", "image": "images/Grocery.webp"},
    ]
    return render(request, 'home.html', {'categories': categories})

def register(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        Customer.objects.create(name=name, email=email, password=password)
        return redirect('login')
    return render(request, 'register.html')


def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            customer = Customer.objects.get(email=email, password=password)
            request.session['customer_id'] = customer.id
            return redirect('home')
        except Customer.DoesNotExist:
            return render(request, 'login.html', {'error': 'Invalid email or password'})
    return render(request, 'login.html')

def search(request):
    return render(request, 'search.html')

def categories(request):
    return render(request, 'categories.html')

def category_products(request, category):
    try:
        category_obj = Category.objects.get(name__iexact=category)
    except Category.DoesNotExist:
        raise Http404("Category not found")

    products = Product.objects.filter(category=category_obj)

    return render(request, 'category_products.html', {
        'products': products,
        'category': category_obj.name,
    })

def product_detail(request, product_id):
    try:

        product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        raise Http404("Product not found")
    
    return render(request, 'product_detail.html', {'product': product})

def add_to_cart(request, product_id):
    if 'customer_id' not in request.session:
        return redirect('login')  # Redirect to login if not logged in

    customer_id = request.session['customer_id']
    customer = Customer.objects.get(id=customer_id)
    product = get_object_or_404(Product, id=product_id)

    cart_item, created = Cart.objects.get_or_create(
        customer=customer,
        product=product,
        defaults={'quantity': 1}
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('view_cart')

def cart(request):
    if 'customer_id' not in request.session:
        return redirect('login')  # Redirect if not logged in

    customer_id = request.session['customer_id']
    customer = Customer.objects.get(id=customer_id)

    cart_items_db = Cart.objects.filter(customer=customer)

    cart_items = []
    total = 0

    for item in cart_items_db:
        item_total = item.product.price * item.quantity
        cart_items.append({
            'product': item.product,
            'quantity': item.quantity,
            'total_price': item_total
        })
        total += item_total

    context = {
        'cart_items': cart_items,
        'total': total
    }

    print("Cart items from DB:", cart_items)
    return render(request, 'cart.html', context)

def remove_from_cart(request, product_id):
    if 'customer_id' not in request.session:
        return redirect('login')

    customer_id = request.session['customer_id']
    customer = Customer.objects.get(id=customer_id)

    try:
        cart_item = Cart.objects.get(customer=customer, product_id=product_id)
        cart_item.delete()
        messages.success(request, 'Product removed from cart.')
    except Cart.DoesNotExist:
        messages.error(request, 'Product not found in your cart.')

    return redirect('view_cart')

def add_to_wishlist(request, product_id):
    if 'customer_id' not in request.session:
        messages.error(request, "You must be logged in to add items to wishlist.")
        return redirect('login')

    customer_id = request.session['customer_id']  # ✅ Fix: get from session
    product = Product.objects.get(id=product_id)

    wishlist_item, created = Wishlist.objects.get_or_create(customer_id=customer_id, product=product)

    if created:
        messages.success(request, "Product added to wishlist.")
    else:
        messages.info(request, "Product is already in your wishlist.")

    return redirect('product_detail', product_id=product.id)

def remove_from_wishlist(request, product_id):
    if 'customer_id' in request.session:
        customer = Customer.objects.get(id=request.session['customer_id'])
        Wishlist.objects.filter(customer=customer, product_id=product_id).delete()

    return redirect('wishlist')

def wishlist(request):
    if 'customer_id' not in request.session:
        return redirect('login')

    customer = Customer.objects.get(id=request.session['customer_id'])
    wishlist_items = Wishlist.objects.filter(customer=customer)

    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})

def move_to_cart(request, product_id):
    customer_id = request.session.get('customer_id')
    if not customer_id:
        return redirect('login')

    # Remove from wishlist
    Wishlist.objects.filter(customer_id=customer_id, product_id=product_id).delete()

    # Add to cart (if not already)
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = Cart.objects.get_or_create(customer_id=customer_id, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, 'Moved to cart.')
    return redirect('view_cart')  # or redirect('wishlist') if you want to stay there

def confirm_order(request):
    if 'customer_id' not in request.session:
        return redirect('login')

    customer_id = request.session['customer_id']
    customer = Customer.objects.get(id=customer_id)

    cart_items = Cart.objects.filter(customer=customer)
    if not cart_items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect('view_cart')

    total = sum(item.product.price * item.quantity for item in cart_items)

    # ✅ If button is clicked (POST), go to Stripe session
    if request.method == 'POST':
        return redirect('create_checkout_session')

    # Optional: Add total price per item to use in template
    for item in cart_items:
        item.total_price = item.product.price * item.quantity

    context = {
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'confirm_order.html', context)
