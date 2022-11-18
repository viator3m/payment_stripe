from django.shortcuts import render, get_object_or_404

from .models import Item


def item_page(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    template = 'payment/item.html'
    context = {
        'item': item
    }

    return render(request, template, context)
