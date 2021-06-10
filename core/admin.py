from django.contrib import admin
from . import models
# Register your models here.


class NodeAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'theme']


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'node', 'first_name', 'last_name']


class AddressAndInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'node', 'city', 'country']


class ThemeDisplay(admin.ModelAdmin):
    list_display = ['name', 'dm', 'dk', 'lt', 'pm', 'sc']


admin.site.register(models.AddressAndInfo, AddressAndInfoAdmin)
admin.site.register(models.Profile, ProfileAdmin)
admin.site.register(models.Theme, ThemeDisplay)
admin.site.register(models.Node, NodeAdmin)
