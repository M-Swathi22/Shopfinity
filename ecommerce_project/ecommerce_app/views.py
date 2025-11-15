from django.shortcuts import render
from django.conf import settings
from django.shortcuts import render,redirect,get_object_or_404
from .models import Customer
from .models import Product,Category

# Create your views here.
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