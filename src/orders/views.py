import time

from decimal import *
from datetime import datetime, timedelta
from django.utils import timezone

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives, EmailMessage
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect 
from django.shortcuts import render, render_to_response, HttpResponseRedirect, RequestContext, Http404, get_object_or_404, redirect
from django.template.loader import render_to_string
from email.MIMEImage import MIMEImage

from .models import Order, ShippingAddress, BillingAddress
from .forms import ShippingAddressForm, BillingAddressForm

from carts.models import Cart, CartItem
from products.models import Variation

from .utils import id_generator

import stripe
import braintree

braintree.Configuration.configure(braintree.Environment.Sandbox,
                                  merchant_id="use_your_merchant_id",
                                  public_key="use_your_public_key",
                                  private_key="use_your_private_key")


def checkout_details(request):
	try:
		the_id = request.session['cart_id']
		cart = Cart.objects.get(id=the_id)
	except:
		the_id = None
		return HttpResponseRedirect(reverse("view_cart"))
	
	try:
		new_order = Order.objects.get(cart=cart)
	except Order.DoesNotExist:
		new_order = Order()
		new_order.cart = cart
		#new_order.user = request.user
		new_order.order_id = id_generator()
		new_order.save()
	except:
		new_order = None
		# work on some error message
		return HttpResponseRedirect(reverse("view_cart"))

	sub_total = 0
	sale_total = 0
	cart_items = CartItem.objects.filter(cart=cart)
	for i in range(len(cart_items)):
		sub_total += cart_items[i].product.price

	if cart.promo_code:
		promo = (Decimal(cart.promo_code.deal) / 100)
		saleTotal = sub_total - (sub_total * promo)
		sale_savings = (sub_total * promo)
		new_order.sale_savings = round(sale_savings, 2)
		new_order.sale_total = round(saleTotal, 2)
	
	new_order.sub_total = sub_total
	new_order.save()

	try:
		shipping_id = new_order.shipping_address.id
		shipping_instance = ShippingAddress.objects.get(id=shipping_id)
	except:
		shipping_instance = None
	
	try:
		billing_id = new_order.billing_address.id
		billing_instance = BillingAddress.objects.get(id=billing_id)
	except:
		billing_instance = None

	if shipping_instance:
		shipping_form = ShippingAddressForm(request.POST or None, instance=shipping_instance)
	else:
		shipping_form = ShippingAddressForm(request.POST)

	if billing_instance:
		billing_form = BillingAddressForm(request.POST or None, instance=billing_instance)
	else:
		billing_form = BillingAddressForm(request.POST)

	if shipping_form.is_valid() and billing_form.is_valid():
		new_shipping = shipping_form.save()
		new_billing = billing_form.save()

		new_order.name = new_shipping.shipping_name
		new_order.shipping_address = new_shipping
		new_order.billing_address = new_billing

		shipping_total = 0
		cart_items = CartItem.objects.filter(cart=cart)
		for i in range(len(cart_items)):
			if i == 0:
				shipping_total += 5
			else:
				shipping_total += 2.5

		new_order.shipping_total = shipping_total

		if cart.promo_code:
			new_order.final_total = (Decimal(new_order.sale_total) + Decimal(shipping_total))
		else:
			new_order.final_total = (Decimal(sub_total) + Decimal(shipping_total))

		new_order.save()


		return HttpResponseRedirect(reverse("checkout_payment", args=(new_order.id,)))

	return render_to_response("orders/checkout_details.html", locals(), context_instance=RequestContext(request))


def client_token(request):
	if request.method == "GET":
		token = braintree.ClientToken.generate()
		return token


def checkout_payment(request, id):
	try:
		the_id = request.session['cart_id']
		cart = Cart.objects.get(id=the_id)
	except:
		the_id = None
		return HttpResponseRedirect(reverse("view_cart"))
	
	try:
		new_order = Order.objects.get(id=id, cart=cart)
	except Order.DoesNotExist:
		new_order = None
		# work on some error message
		return HttpResponseRedirect(reverse("view_cart"))

	token = braintree.ClientToken.generate()

	if request.method == "POST":
		nonce = request.POST["payment_method_nonce"]
		result = braintree.Transaction.sale(
			{
				"amount": str(new_order.final_total),
				"payment_method_nonce": nonce,
			    "options": {
			        "submit_for_settlement": "true"
			    }
			}
		)

		if result.is_success:
			new_order.status = "Finished"
			new_order.save()

			#Remove 1 of each item
			cart_items = CartItem.objects.filter(cart=cart)
			for item in cart_items:
				if item.variations:
					variation_id = item.variations.id
					variation = Variation.objects.get(id=variation_id) 
					variation.quantity -= item.quantity
					variation.save()

			#send email
			site = "http://www.your-domain-here.com/"
			ctx_dict = {'new_order': new_order, 'cart_items': cart_items}
			message_html = render_to_string('emails/order_confirmation.html', ctx_dict)
			msg = mail.EmailMessage("New Order", message_html, settings.DEFAULT_FROM_EMAIL, ['your-email-address@your-host.com'])
			msg.content_subtype = "html"
			msg.send()

			del request.session['cart_id']
			del request.session['items_total']

			messages.success(request, "Thank your order. It has been completed!")
			return HttpResponseRedirect(reverse("checkout_confirmation", args=(new_order.id,)))
		else:
			messages.success(request, result.message)


	return render_to_response("orders/checkout.html", locals(), context_instance=RequestContext(request))

def checkout_confirmation(request, id):
	new_order = get_object_or_404(Order, id=id)
	cart_id = new_order.cart.id
	cart = get_object_or_404(Cart, id=cart_id)
	return render_to_response("orders/checkout_confirmation.html", locals(), context_instance=RequestContext(request))



