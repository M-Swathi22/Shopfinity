from django.contrib import admin
from .models import Category, Product,Customer,Cart,Wishlist

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Cart)
admin.site.register(Wishlist)
