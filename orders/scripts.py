
import xmltodict
import urllib
import datetime
import logging

from .models import Order


def create_order(data):
    Order.objects.create(
        order_id=data["order_id"],
        marketplace=data["marketplace"],
        order_status_marketplace=data["order_status_marketplace"],
        order_status_lengow=data["order_status_lengow"],
        order_purchase_date=data["order_purchase_date"],
        billing_email=data["billing_email"],
        delivery_full_address=data["delivery_full_address"],
        first_product_title=data["first_product_title"],
        first_product_category=data["first_product_category"],
        first_product_url_image=data["first_product_url_image"],
    )


def update_order(order, data):
    order.marketplace = data["marketplace"]
    order.order_status_marketplace = data["order_status_marketplace"]
    order.order_status_lengow = data["order_status_lengow"]
    order.order_purchase_date = data["order_purchase_date"]
    order.billing_email = data["billing_email"]
    order.delivery_full_address = data["delivery_full_address"]
    order.first_product_title = data["first_product_title"]
    order.first_product_category = data["first_product_category"]
    order.first_product_url_image = data["first_product_url_image"]
    order.update_time = datetime.datetime.now()
    order.save()


def insert_or_update_order(data):
    order = Order.objects.filter(order_id=data["order_id"])
    if not order.exists():
        create_order(data)
    else:
        order = order.first()
        update_order(order, data)


def load_one_order(order):
    data = {}
    data["marketplace"] = order["marketplace"]
    data["order_status_marketplace"] = order["order_status"]["marketplace"]
    data["order_status_lengow"] = order["order_status"]["lengow"]
    data["order_id"] = order["order_id"]
    date_purchase = str(order["order_purchase_date"])
    h_purchase = str(order["order_purchase_heure"])
    date_h_purchase = date_purchase + "-" + h_purchase
    try:
        datetime_purchase = datetime.datetime.strptime(date_h_purchase,
                                                       "%Y-%m-%d-%H:%M:%S")
    except ValueError as e:
        logging.error(str(e))
        datetime_purchase = None
    data["order_purchase_date"] = datetime_purchase
    data["billing_email"] = order["billing_address"]["billing_email"]
    data["delivery_full_address"] = \
        order["delivery_address"]["delivery_full_address"]
    nb_product = int(order["cart"]["nb_orders"])
    if nb_product == 1:
        product_info = order["cart"]["products"]["product"]
    else:
        product_info = order["cart"]["products"]["product"][0]
    data["first_product_title"] = product_info["title"]
    data["first_product_category"] = product_info["category"]
    data["first_product_url_image"] = product_info["url_image"]
    insert_or_update_order(data)


def load_xml_url(url_file):
    try:
        data = urllib.request.urlopen(url_file)
        data_xml = xmltodict.parse(data.read())
        nb_order = int(data_xml["statistics"]["orders_count"]["count_total"])
        if nb_order == 0:
            return
        elif nb_order == 1:
            load_one_order(data_xml["statistics"]["orders"]["order"])
        else:
            list_orders = data_xml["statistics"]["orders"]["order"]
            for order in list_orders:
                load_one_order(order)
    except Exception as e:
        print(str(e))


if __name__ == '__main__':
    load_xml_url("http://test.lengow.io/orders-test.xml")
