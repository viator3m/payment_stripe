from django.urls import path

from . import views

app_name = 'payment'

urlpatterns = [
    path('item/<int:item_id>/', views.item_page, name='item'),
    path('buy/<int:item_id>/', views.buy_item, name='buy'),
    path('success/', views.success, name='success'),
    path('cancel/', views.cancel, name='cancel'),
    path('', views.index, name='index'),
]
