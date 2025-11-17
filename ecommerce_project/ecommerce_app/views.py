from django.shortcuts import render,redirect,get_object_or_404
from .models import Customer
from .models import Product,Category
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
