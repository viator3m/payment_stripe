import stripe
from django.urls import reverse
from stripe.error import InvalidRequestError
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from payment_server.settings import STRIPE_API_KEY
from .models import Item, Order, OrderItem


def index(request):
    items = Item.objects.all()
    return render(request, 'payment/index.html', {'items': items})


def success(request):
    return render(request, 'payment/success.html',)


def cancel(request):
    return render(request, 'payment/cancel.html',)


def item_page(request, item_id):
    order = Order.objects.last()
    item = get_object_or_404(Item, pk=item_id)
    template = 'payment/item.html'
    in_order = item in order.item.all()

    context = {
        'item': item,
        'in_order': in_order
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


def add_to_order(request, item_id):
    order = Order.objects.last()
    if order is None or order.payed:
        order = Order.objects.create()
    item = get_object_or_404(Item, id=item_id)

    OrderItem.objects.create(order=order, item=item)
    order.total += item.price
    order.save()

    url = reverse('payment:item', args=(item_id, ))
    return redirect(url)


def delete_from_order(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    order = Order.objects.last()

    OrderItem.objects.get(item=item, order=order).delete()
    order.total -= item.price
    order.save()

    url = reverse('payment:item', args=(item_id, ))
    return redirect(url)


def order_page(request):
    order = Order.objects.last()
    if order is None or order.payed:
        order = Order.objects.create()
    items = order.item.all()
    template = 'payment/order.html'
    return render(request, template, {'items': items})


def buy_order(request):
    order = Order.objects.last()
    if order is None:
        return redirect(reverse('payment:order'))

    item_list = ', '.join(
        [name[0] for name in OrderItem.objects.filter(
            order=order
        ).values_list('item__name')]
    )
    stripe.api_key = STRIPE_API_KEY
    domain = f'http://{request.get_host()}'

    try:
        session = stripe.checkout.Session.create(
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': item_list,
                    },
                    'unit_amount': order.total,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=f'{domain}/success/',
            cancel_url=f'{domain}/cancel/',
        )
    except InvalidRequestError as error:
        return HttpResponse({'error': error})

    order.payed = True
    order.save()
    return JsonResponse({'session_id': session.id})
