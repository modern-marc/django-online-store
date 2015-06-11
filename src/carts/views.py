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

# Create your views here.

from products.models import Product, Variation

from .models import Cart, CartItem, PromoCode

def view_cart(request):
	try:
		the_id = request.session['cart_id']
		cart = Cart.objects.get(id=the_id)
	except:
		the_id = None
		
	if the_id:
		new_total = 0.00
		for item in cart.cartitem_set.all():
			line_total = float(item.product.price) * item.quantity
			new_total += line_total
		request.session['items_total'] = cart.cartitem_set.count()
		if cart.promo_code:
			cart.total = new_total - (new_total * (cart.promo_code.deal / 100))
		else:
			cart.total = new_total
		cart.save()
	else:
		empty_message = "Your Cart is Empty, please keep shopping."
		empty = True

	return render_to_response("cart/view_cart.html", locals(), context_instance=RequestContext(request))

		
def add_promo(request):
	if request.method == "POST":
		code = request.POST["code"]
		try:
			promo_code = PromoCode.objects.get(code=code)
		except:
			messages.success(request, 'Sorry, Not a valid code.')
			return HttpResponseRedirect(reverse("checkout_details")) 

		if promo_code:
			try:
				the_id = request.session['cart_id']
				cart = Cart.objects.get(id=the_id)
			except:
				messages.success(request, 'Sorry, not a valid cart.')
				return HttpResponseRedirect(reverse("view_cart")) 

			if cart:
				cart.promo_code = promo_code
				cart.total = cart.total - (cart.total * (promo_code.deal / 100))
				cart.save()
				messages.success(request, 'Promo Code Applied')
				return HttpResponseRedirect(reverse("checkout_details")) 


def remove_promo(request):
	try:
		the_id = request.session['cart_id']
		cart = Cart.objects.get(id=the_id)
	except:
		messages.success(request, 'Sorry, not a valid cart.')
		return HttpResponseRedirect(reverse("view_cart"))

	if cart.promo_code:
		cart.promo_code = None
		cart.sale_total = None
		cart.save() 
		messages.success(request, 'Promo Code Removed')
		return HttpResponseRedirect(reverse("checkout_details")) 


def remove_from_cart(request, id):
	if request.method == "POST":
		try:
			the_id = request.session['cart_id']
			cart = Cart.objects.get(id=the_id)
		except:
			return HttpResponseRedirect(reverse("cart"))

		cartitem = CartItem.objects.get(id=id)
		cartitem.cart = None
		cartitem.save()
		return HttpResponseRedirect(reverse("view_cart"))


def add_to_cart(request, slug):
	request.session.set_expiry(120000)

	try:
		the_id = request.session['cart_id']
	except:
		new_cart = Cart()
		new_cart.save()
		request.session['cart_id'] = new_cart.id
		the_id = new_cart.id
	
	cart = Cart.objects.get(id=the_id)

	try:
		product = Product.objects.get(slug=slug)
	except Product.DoesNotExist:
		pass
	except:
		pass

	if request.method == "POST":
		qty = request.POST['qty']
		size = request.POST["size"]
		product_variation = None
		cart_item = None

		try:
			variation = Variation.objects.get(product=product, size__iexact=size)
			product_variation = variation
		except:
			pass

		if product_variation.quantity == 0 or product_variation == None:
			messages.success(request, 'Sorry, that size is no longer available.')
			return HttpResponseRedirect(reverse("view_cart"))
		elif int(qty) > product_variation.quantity:
			messages.success(request, 'Sorry, that size is not available in that quantity.')
			return HttpResponseRedirect(reverse("view_cart"))
			
		try:
			print "trying to find cart item"
			cart_item = CartItem.objects.get(cart=cart, product=product, variations=product_variation)
			print "cart item found"
			ciq = cart_item.quantity
			cart_item.quantity = ciq + qty
			print "cart item quantity updated"
			if cart_item.quantity > product_variation.quantity:
				messages.success(request, 'Sorry, that size is not available in that quantity.')
				return HttpResponseRedirect(reverse("view_cart"))
		except:
			print "creating new cart item"
			cart_item = CartItem.objects.create(cart=cart, product=product, variations=product_variation)
			cart_item.quantity = qty
		cart_item.save()
		return HttpResponseRedirect(reverse("view_cart"))
	return HttpResponseRedirect(reverse("view_cart"))