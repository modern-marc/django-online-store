from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save


class Product(models.Model):
	title = models.CharField(max_length=120)
	description = models.TextField(null=True, blank=True)
	price = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)
	sale_price = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
	shipping_price = models.DecimalField(decimal_places=2, max_digits=10, default=5.00)
	slug = models.SlugField(unique=True)
	order = models.IntegerField(unique=True, null=True, blank=True)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)
	active = models.BooleanField(default=True)

	def __unicode__(self):
		return self.title

	class Meta:
		unique_together = ('title', 'slug')

	class Meta:
		ordering = ['order']

	def get_price(self):
		return self.price

	def get_absolute_url(self):
		return reverse("single_product", kwargs={"slug": self.slug})


class ProductImage(models.Model):
	product = models.ForeignKey(Product)
	image = models.ImageField(upload_to='products/images/')
	featured = models.BooleanField(default=False)
	active = models.BooleanField(default=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)

	def __unicode__(self):
		return self.product.title


SIZES = (
	('X-Small', 'X-Small'),
	('Small', 'Small'),
	('Medium', 'Medium'),
	('Large', 'Large'),
	('X-Large', 'X-Large'),
	('XX-Large', 'XX-Large'),
	('XXX-Large', 'XX-Large'),
)

class Variation(models.Model):
	product = models.ForeignKey(Product)
	size = models.CharField(max_length=120, default="Large", choices=SIZES)
	image = models.ForeignKey(ProductImage, null=True, blank=True)
	price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
	quantity = models.IntegerField(default=0)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)
	active = models.BooleanField(default=False)

	def __unicode__(self):
		return self.size

