from django.contrib import admin
from .models import TelegramUser, Coffee, Addon, Order, OrderItem

# Register your models here.
admin.site.register((TelegramUser, Coffee, Addon, Order, OrderItem))
