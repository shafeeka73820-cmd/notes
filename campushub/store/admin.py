from django.contrib import admin
from .models import Category, Product, Cart, CartItem, Order, OrderItem

admin.site.register([Category, Product, Cart, CartItem, Order, OrderItem])
