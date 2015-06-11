from django.contrib import admin

# Register your models here.
from .models import Product, ProductImage, Variation

class ProductImageInline(admin.TabularInline):
	model = ProductImage

class VariationInline(admin.TabularInline):
	model = Variation

class ProductAdmin(admin.ModelAdmin):
	inlines = [ProductImageInline, VariationInline]
	date_hierarchy = 'timestamp' #updated
	search_fields = ['title', 'description']
	list_display = ['title', 'price', 'order', 'active', 'updated']
	list_editable = ['price', 'order', 'active']
	list_filter = ['price', 'active']
	readonly_fields = ['updated', 'timestamp']
	prepopulated_fields = {"slug": ("title",)}
	class Meta:
		model = Product

admin.site.register(Product, ProductAdmin)