from django.urls import path
from . import views

urlpatterns = [
     path('', views.home, name='home'),
     path('register/', views.register, name='register'),
     path('login/', views.login_view, name='login'),
     path('categories/',views.categories,name='categories'),
     path('categories/<str:category>/', views.category_products, name='category_products'),
     path('search/', views.search, name='search'),
     

]