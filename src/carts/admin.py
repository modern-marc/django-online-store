from django.contrib import admin

# Register your models here.

from .models import Cart, CartItem, PromoCode

class CartAdmin(admin.ModelAdmin):
	class Meta:
		model = Cart


admin.site.register(Cart, CartAdmin)


admin.site.register(CartItem)
admin.site.register(PromoCode)