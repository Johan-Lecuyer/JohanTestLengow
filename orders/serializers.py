from rest_framework import serializers

from .models import Order


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Order
        fields = ('order_id',
                  'marketplace',
                  'order_status_marketplace',
                  'order_status_lengow',
                  'order_purchase_date',
                  'billing_email',
                  'delivery_full_address',
                  'first_product_title',
                  'first_product_category',
                  'first_product_url_image')
