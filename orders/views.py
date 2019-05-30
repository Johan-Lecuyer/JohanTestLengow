from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from rest_framework import viewsets

from .forms import FluxXMLForm

from .scripts import load_xml_url

from .models import Order

from .serializers import OrderSerializer


class OrderViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Order.objects.all().order_by('-order_purchase_date')
    serializer_class = OrderSerializer


def add_paginator(request, orders):
    paginator = Paginator(orders, 9)
    page = request.GET.get('page')
    try:
        orders = paginator.page(page)
    except PageNotAnInteger:
        orders = paginator.page(1)
    except EmptyPage:
        orders = paginator.page(paginator.num_pages)
    return orders


def index(request):
    context = {'current_page': 'home'}
    orders = Order.objects.all().order_by('-order_purchase_date')
    orders = add_paginator(request, orders)
    context["orders"] = orders
    context["paginate"] = True
    return render(request, 'orders/index.html', context)


def search(request):
    context = {'current_page': 'home'}
    query = request.GET.get('query')
    title = "Résultats pour la recherche %s" % query
    if not query:
        orders = Order.objects.all()
    else:
        # title contains the query is and query is not sensitive to case.
        orders = Order.objects.filter(order_id__icontains=query) | \
            Order.objects.filter(order_status_marketplace__icontains=query) | \
            Order.objects.filter(order_status_lengow__icontains=query) | \
            Order.objects.filter(first_product_title__icontains=query) | \
            Order.objects.filter(first_product_category__icontains=query)
    orders = add_paginator(request, orders)
    context["orders"] = orders
    context["paginate"] = True
    context['title'] = title
    return render(request, 'orders/search.html', context)


def load_flux_xml(request):
    context = {'current_page': 'load_flux_xml'}
    if request.method == 'POST':
        form = FluxXMLForm(request.POST)
        if form.is_valid():
            flux_url = form.cleaned_data['flux_url']
            load_xml_url(flux_url)
        else:
            context['errors'] = form.errors.items()
    else:
        form = FluxXMLForm()
    context['form'] = form
    return render(request, 'orders/load_flux_xml.html', context)


def detail(request, id):
    context = {'current_page': 'detail'}
    order = get_object_or_404(Order, pk=id)
    context['order'] = order
    return render(request, 'orders/detail.html', context)
