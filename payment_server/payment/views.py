import stripe
from stripe.error import InvalidRequestError
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404

from payment_server.settings import STRIPE_API_KEY
from .models import Item


def index(request):
    return render(request, 'payment/index.html',)


def success(request):
    return render(request, 'payment/success.html',)


def cancel(request):
    return render(request, 'payment/cancel.html',)


def item_page(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    template = 'payment/item.html'
    context = {
        'item': item
    }

    return render(request, template, context)


def buy_item(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    stripe.api_key = STRIPE_API_KEY
    domain = f'http://{request.get_host()}'

    try:
        session = stripe.checkout.Session.create(
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': item.name,
                    },
                    'unit_amount': item.price,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=f'{domain}/success/',
            cancel_url=f'{domain}/cancel/',
        )
    except InvalidRequestError as error:
        return HttpResponse({'error': error})
    return JsonResponse({'session_id': session.id})
