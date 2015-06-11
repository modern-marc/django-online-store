from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('carts.views',
    url(r'^$', 'view_cart', name='view_cart'),
    url(r'^add/(?P<slug>[\w-]+)/$', 'add_to_cart', name='add_to_cart'),
    url(r'^add_promo/$', 'add_promo', name='add_promo'),
    url(r'^remove_promo/$', 'remove_promo', name='remove_promo'),
    url(r'^remove/(?P<id>\d+)/$', 'remove_from_cart', name='remove_from_cart'),
) 

