from decimal import Decimal
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

from carts.models import Cart


STATUS_CHOICES = (
		("Started", "Started"),
		("Abandoned", "Abandoned"),
		("Finished", "Finished"),
	)

class ShippingAddress(models.Model):
	shipping_user = models.ForeignKey(User, null=True, blank=True)
	shipping_name = models.CharField(max_length=200)
	shipping_address = models.CharField(max_length=120)
	shipping_address2 = models.CharField(max_length=120, null=True, blank=True)
	shipping_city = models.CharField(max_length=120)
	shipping_state = models.CharField(max_length=120)
	shipping_country = models.CharField(max_length=120)
	shipping_zipcode = models.CharField(max_length=25)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)

	def __unicode__(self):
		return self.get_address()

	def get_address(self):
		return "%s, %s, %s, %s, %s, %s" %(self.shipping_name, self.shipping_address, self.shipping_city, self.shipping_state, self.shipping_country, self.shipping_zipcode)

class BillingAddress(models.Model):
	billing_user = models.ForeignKey(User, null=True, blank=True)
	billing_name = models.CharField(max_length=200)
	billing_address = models.CharField(max_length=120)
	billing_address2 = models.CharField(max_length=120, null=True, blank=True)
	billing_city = models.CharField(max_length=120)
	billing_state = models.CharField(max_length=120)
	billing_country = models.CharField(max_length=120)
	billing_zipcode = models.CharField(max_length=25)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)

	def __unicode__(self):
		return self.get_address()

	def get_address(self):
		return "%s, %s, %s, %s, %s, %s" %(self.billing_name, self.billing_address, self.billing_city, self.billing_state, self.billing_country, self.billing_zipcode)

class Order(models.Model):
	user = models.ForeignKey(User, blank=True, null=True)
	name = models.CharField(max_length=200)
	order_id = models.CharField(max_length=120, default='ABC', unique=True)
	cart = models.ForeignKey(Cart)
	status = models.CharField(max_length=120, choices=STATUS_CHOICES, default="Started")
	shipping_address = models.ForeignKey(ShippingAddress, blank=True, null=True)
	billing_address = models.ForeignKey(BillingAddress, blank=True, null=True)
	sub_total = models.DecimalField(default=0.00, max_digits=50, decimal_places=2)
	sale_total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
	sale_savings = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
	shipping_total = models.DecimalField(default=0.00, max_digits=50, decimal_places=2)
	final_total = models.DecimalField(default=0.00, max_digits=50, decimal_places=2)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)

	def __unicode__(self):
		return self.order_id

	#def get_final_amount(self):
	#	instance = Order.objects.get(id=self.id)
	#	two_places = Decimal(10) ** -2
	#	tax_rate_dec = Decimal("%s" %(0.089))
	#	sub_total_dec = Decimal(self.sub_total)
	#	tax_total_dec = Decimal(tax_rate_dec * sub_total_dec).quantize(two_places)
	#	instance.tax_total = tax_total_dec
	#	instance.final_total = sub_total_dec + tax_total_dec
	#	instance.save()
	#	return instance.final_total

