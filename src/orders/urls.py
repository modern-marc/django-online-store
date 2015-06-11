from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('orders.views',
    url(r'^checkout-details/$', 'checkout_details', name='checkout_details'),
    url(r'^checkout/(?P<id>\d+)/$', 'checkout_payment', name='checkout_payment'),
    url(r'^checkout-confirm/(?P<id>\d+)/$', 'checkout_confirmation', name='checkout_confirmation'),
    url(r'^$', 'orders', name='user_orders'),
) 

