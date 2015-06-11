from django import forms
from django.forms import ModelForm

from .models import ShippingAddress, BillingAddress

class ShippingAddressForm(ModelForm):
	class Meta:
		model = ShippingAddress
		fields = ('shipping_name', 'shipping_address', 'shipping_address2', 'shipping_city', 'shipping_state', 'shipping_country', 'shipping_zipcode',)

class BillingAddressForm(ModelForm):
	class Meta:
		model = BillingAddress
		fields = ('billing_name', 'billing_address', 'billing_address2', 'billing_city', 'billing_state', 'billing_country', 'billing_zipcode',)