from django.db import models

# Create your models here.
from products.models import Product, Variation

class CartItem(models.Model):
	cart = models.ForeignKey('Cart', null=True, blank=True)
	product = models.ForeignKey(Product)
	variations = models.ForeignKey(Variation, null=True, blank=True)
	quantity = models.IntegerField(default=1)
	line_total = models.DecimalField(default=0.00, max_digits=50, decimal_places=2)
	notes = models.TextField(null=True, blank=True)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)

	def __unicode__(self):
		try:
			return str(self.cart.id)
		except:
			return self.product.title

class PromoCode(models.Model):
	code = models.CharField(max_length=100)
	deal = models.IntegerField(default=0)

	def __unicode__(self):
		return "Deal %d percent" %(self.deal)


class Cart(models.Model):
	total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
	sale_total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
	promo_code = models.ForeignKey(PromoCode, null=True, blank=True)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)
	active = models.BooleanField(default=True)

	def __unicode__(self):
		return "Cart id: %s" %(self.id)