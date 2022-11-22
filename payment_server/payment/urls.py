from django.urls import path

from . import views

app_name = 'payment'

urlpatterns = [
    path('item/<int:item_id>/', views.item_page, name='item'),
    path('buy/<int:item_id>/', views.buy_item, name='buy'),

    path('item/<int:item_id>/add/', views.add_to_order, name='add_to_order'),
    path('item/<int:item_id>/delete/', views.delete_from_order, name='delete_from_order'), # noqa

    path('order/', views.order_page, name='order'),
    path('order/buy/', views.buy_order, name='buy_order'),

    path('success/', views.success, name='success'),
    path('cancel/', views.cancel, name='cancel'),

    path('', views.index, name='index'),
]
