from django.core.validators import MinValueValidator
from django.db import models


class Item(models.Model):
    """Класс единицы товара."""
    name = models.CharField(
        verbose_name='Имя',
        max_length=255,
        unique=True,
    )
    description = models.TextField(
        verbose_name='Описание'
    )
    price = models.PositiveSmallIntegerField(
        verbose_name='Цена',
    )

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return f'{self.name}: {self.description[:100]}'


class Order(models.Model):
    item = models.ManyToManyField(
        Item,
        verbose_name='Товар',
        related_name='order'
    )
    amount = models.PositiveSmallIntegerField(
        default=0,
        verbose_name='Сумма заказа',
        validators=((MinValueValidator(
            limit_value=0.01,
            message='Сумма заказа должна быть больше нуля.'
            )
        ),)
    )

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'{self.item.name}'
