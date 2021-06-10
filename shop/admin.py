from django.contrib import admin
from . import models


class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'price', 'slug',
        'discounted_price'
    ]
    exclude = ['discounted_price']

    prepopulated_fields = {
        'slug': ('name',),
    }


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    prepopulated_fields = {'slug': ('name',)}

    class Meta:
        exclude = ('slug',)


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'owner', 'name', 'price', 'ordered']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'owner', 'price', 'items_count', 'ref_code']


class WishAdmin(admin.ModelAdmin):
    list_display = ['id', 'owner', 'item']


class CouponAdmin(admin.ModelAdmin):
    list_display = ["id", "code", "applied", "usage"]


class BannerAdmin(admin.ModelAdmin):
    list_display = ["id", "expired"]


class BrandAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]


admin.site.register(models.WishList, WishAdmin)
admin.site.register(models.OrderItem, OrderItemAdmin)
admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Banner, BannerAdmin)
admin.site.register(models.Brand, BrandAdmin)
admin.site.register(models.Coupon, CouponAdmin)
