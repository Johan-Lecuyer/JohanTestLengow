from django.contrib import admin

from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_filter = ['marketplace', 'order_purchase_date', 'order_status_lengow']
