import os

from decimal import *
from datetime import datetime, timedelta
from django.utils import timezone

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives, EmailMessage
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect 
from django.shortcuts import render, render_to_response, HttpResponseRedirect, RequestContext, Http404, get_object_or_404, redirect
from django.template.loader import render_to_string
from email.MIMEImage import MIMEImage


from .models import Product, ProductImage, Variation


def home(request):
	featured_products = Product.objects.all()[:3]
	return render_to_response("home.html", locals(), context_instance=RequestContext(request))


def all_products(request):
	products = Product.objects.all()
	return render_to_response("products/all.html", locals(), context_instance=RequestContext(request))


def single_product(request, slug):
	try:
		product = Product.objects.get(slug=slug)
		images = ProductImage.objects.filter(product=product)
		variations = Variation.objects.filter(product=product)
		return render_to_response("products/single.html", locals(), context_instance=RequestContext(request))
	except:
		raise Http404
