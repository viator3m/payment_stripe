from django.contrib import admin

from .models import Item, Order


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'description', 'price')
    list_display_links = ('name', )
    search_fields = ('name', )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('pk', 'display_items', 'total', 'payed')
    search_fields = ('pk', )

    def display_items(self, obj):
        return ', '.join([item.name for item in obj.item.all()])
    display_items.short_description = 'Товары'


