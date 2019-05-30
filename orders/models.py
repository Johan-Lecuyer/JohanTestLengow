from django.db import models


class Order(models.Model):
    marketplace = models.CharField(max_length=300, null=True)
    order_status_marketplace = models.CharField(max_length=100, null=True)
    order_status_lengow = models.CharField(max_length=100, null=True)
    order_id = models.CharField(max_length=300, unique=True)
    order_purchase_date = models.DateTimeField(null=True)
    billing_email = models.EmailField(max_length=300, null=True)
    delivery_full_address = models.CharField(max_length=300, null=True)
    first_product_title = models.CharField(max_length=300, null=True)
    first_product_category = models.CharField(max_length=300, null=True)
    first_product_url_image = models.URLField(max_length=10000, null=True)
    registery_time = models.DateTimeField(auto_now_add=True, null=True)
    update_time = models.DateTimeField(auto_now_add=True, null=True)
