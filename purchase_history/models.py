from django.contrib.auth import get_user_model
from django.db import models

'''
Модель для описания товара
'''


class Product(models.Model):
    vendor_code = models.CharField(max_length=255, null=True, blank=True, verbose_name='Артикул товара')

    title = models.CharField(max_length=255, null=True, blank=True, verbose_name='Название товара')

    brand = models.CharField(max_length=255, null=True, blank=True, verbose_name='Производитель/Бренд товара')

    created_at = models.DateField(auto_now=True, verbose_name='Дата товара')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = "01 Товар"
        verbose_name_plural = "01 Товары"
        ordering = ['brand']


'''
Модель для списка товаров (Корзина)
'''


class ProductList(models.Model):
    product = models.ForeignKey('purchase_history.Product', on_delete=models.PROTECT,
                                verbose_name='Товар', related_name='product_list')

    quantity_product = models.PositiveIntegerField(verbose_name='Количества товара')

    price = models.DecimalField(null=True, blank=True,
                                max_digits=19, decimal_places=2,
                                verbose_name='Стоимость товара за 1 единицу/штуку')

    created_at = models.DateField(auto_now=True, verbose_name='Дата создания списка товара')

    # def __str__(self):
    #     return f'Список товаров покупателя {self.user} за {self.created_at}'

    class Meta:
        verbose_name = "02 Список товаров"
        verbose_name_plural = "02 Список товаров"
        ordering = ['created_at']


'''
Модель для стоимости товара
'''


class PriceProduct(models.Model):
    product = models.ForeignKey('purchase_history.Product', on_delete=models.CASCADE,
                                verbose_name='Товар', related_name='prices')

    price = models.DecimalField(null=True, blank=True,
                                max_digits=19, decimal_places=2,
                                verbose_name='Стоимость товара за 1 единицу/штуку')
    price_date = models.DateField(null=True, blank=True, verbose_name='Дата добавления цены')
    created_at = models.DateField(auto_now=True, verbose_name='Дата создания цены')

    def __str__(self):
        return f'{self.price} - {self.price_date}'

    class Meta:
        verbose_name = "03 Стоимость товара за 1 единицу/штуку"
        verbose_name_plural = "03 Стоимости товаров за 1 единицу/штуку"
        ordering = ['price_date']
