from django.conf import settings
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('contact.views',
    url(r'^$', 'contact', name="contact"),
    url(r'contact_success/$', 'contact_success', name="contact_success")
)