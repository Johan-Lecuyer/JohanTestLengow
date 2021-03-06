from django.test import TestCase
from django.urls import reverse

from .models import Order

# Create your tests here.


class IndexPageTestCase(TestCase):
    def test_index_page(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)


class DetailPageTestCase(TestCase):

    # ran before each test.
    def setUp(self):
        Order.objects.create(marketplace="test", order_id="ID TEST")
        self.order = Order.objects.get(order_id="ID TEST")

    # test that detail page returns a 200 if the item exists
    def test_detail_page_returns_200(self):
        order_pk_id = self.order.id
        response = self.client.get(reverse('orders:detail',
                                           args=(order_pk_id,)))
        self.assertEqual(response.status_code, 200)

    # test that detail page returns a 404 if the item does not exist
    def test_detail_page_returns_404(self):
        order_pk_id = self.order.id + 1
        response = self.client.get(reverse('orders:detail',
                                           args=(order_pk_id,)))
        self.assertEqual(response.status_code, 404)
