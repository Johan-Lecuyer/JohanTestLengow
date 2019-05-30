from django.conf.urls import url
from rest_framework import routers
from django.urls import include
from . import views


router = routers.DefaultRouter()
router.register(r'orders', views.OrderViewSet)


urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
    url(r'^search/$', views.search, name='search'),
    url(r'^detail/(?P<id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^load_flux_xml/$', views.load_flux_xml, name='load_flux_xml'),
]
