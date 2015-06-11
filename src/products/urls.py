from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('products.views',
    url(r'^$', 'all_products', name='all_products'),
    url(r'^(?P<slug>[\w-]+)/$', 'single_product', name='single_product'),
) 

