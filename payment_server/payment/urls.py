from django.urls import path

from . import views

app_name = 'payment'

urlpatterns = [
    path('item/<int:item_id>', views.item_page)
]
