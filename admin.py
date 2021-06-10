from django.contrib import admin
from .models import (
    Product, Category, Order,
    OrderItem, WishList, Banner,
    Parent
)
# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category', 'price', 'slug', 'discounted_price']
    exclude = ['discounted_price']

    prepopulated_fields = {
        'slug': ('name',),
    }


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

    class Meta:
        exclude = ('slug',)


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['owner', 'item', 'is_ordered', 'price']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['ref_code', 'is_processed', 'owner', 'price']


class WishAdmin(admin.ModelAdmin):
    list_display = ['owner', 'item']


admin.site.register(WishList, WishAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Banner)
admin.site.register(Parent)
