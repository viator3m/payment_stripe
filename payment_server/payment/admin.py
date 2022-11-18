from django.contrib import admin

from .models import Item


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'description', 'price')
    list_display_links = ('name', )
    search_fields = ('name', )


