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
