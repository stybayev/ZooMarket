from django.contrib.auth import get_user_model
from django.db import models

'''
Модель для описания товара
'''


class Product(models.Model):
    product_list = models.ForeignKey('purchase_history.ProductList', on_delete=models.CASCADE,
                                     null=True, blank=True, verbose_name='Список товаров',
                                     related_name='product_descriptions')

    vendor_code = models.CharField(max_length=255, null=True, blank=True, verbose_name='Артикул товара')

    title = models.CharField(max_length=255, null=True, blank=True, verbose_name='Название товара')

    brand = models.CharField(max_length=255, null=True, blank=True, verbose_name='Производитель/Бренд товара')

    created_at = models.DateField(auto_now=True, verbose_name='Дата товара')

    def __str__(self):
        return f'Товар{self.title}'

    class Meta:
        verbose_name = "01 Описание товара"
        verbose_name_plural = "01 Описания товаров"
        ordering = ['brand']


'''
Модель для списка товаров (Корзина)
'''


class ProductList(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                             verbose_name='Покупатель', related_name='product_list')
    created_at = models.DateField(auto_now=True, verbose_name='Дата создания списка товара')

    def __str__(self):
        return f'Список товаров покупателя {self.user} за {self.created_at}'

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


'''
Модель для количества товаров
'''


class QuantityProduct(models.Model):
    product_list = models.ForeignKey('purchase_history.ProductList', on_delete=models.CASCADE,
                                     null=True, blank=True, verbose_name='Список товаров',
                                     related_name='quantity_product')

    product = models.ForeignKey('purchase_history.Product', on_delete=models.CASCADE,
                                verbose_name='Товар', related_name='quantity_product')

    quantity_product = models.PositiveIntegerField(verbose_name='Количества товаров')

    created_at = models.DateField(auto_now=True, verbose_name='Дата добавления количества')

    def __str__(self):
        return f'Продукт - {self.product}/Количество - {self.quantity_product}'

    class Meta:
        verbose_name = "04 Количество товара"
        verbose_name_plural = "04 Количества товаров"
        ordering = ['created_at']
