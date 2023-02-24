from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

'''
Модель для описания точки продаж.
Описывает торговую точку с title полем.
'''


class PointOfSale(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название точки продаж')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = "Точка продаж"
        verbose_name_plural = "Точки продаж"


'''
Модель Purchase описывает покупку с такими полями, как date, point_of_sale, 
user, total_cost, discount, total_cost_with_discountи accumulated_bonuses. 
'''


class Purchase(models.Model):
    date = models.DateTimeField(verbose_name='Дата покупки')
    point_of_sale = models.ForeignKey(PointOfSale, on_delete=models.PROTECT, verbose_name='Точка продаж')
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Покупатель')
    total_cost = models.DecimalField(max_digits=19, decimal_places=2, verbose_name='Сумма покупки без скидки')
    discount = models.DecimalField(max_digits=19, decimal_places=2, verbose_name='Сумма скидки')
    total_cost_with_discount = models.DecimalField(max_digits=19, decimal_places=2,
                                                   verbose_name='Сумма покупки со скидкой')
    accumulated_bonuses = models.IntegerField(verbose_name='Накопленные бонусы')

    class Meta:
        verbose_name = "История покупок"
        verbose_name_plural = "История покупок"


'''
Модель Product описывает продукт с такими полями vendor_code, как title, и brand. 
'''


class Product(models.Model):
    vendor_code = models.CharField(max_length=255, verbose_name='Артикул товара')
    title = models.CharField(max_length=255, verbose_name='Название товара')
    brand = models.CharField(max_length=255, verbose_name='Производитель/Бренд товара')
    created_at = models.DateField(auto_now=True, verbose_name='Дата товара')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ['brand']


'''
Модель ProductInPurchase представляет собой список продуктов в покупке и включает ссылку на 
Purchase модель через внешний ключ и на Product модель через другой внешний ключ. 
Каждый ProductInPurchase экземпляр имеет quantity поле и price поле для указания стоимости каждого элемента в списке.
'''


class ProductInPurchase(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, verbose_name='Покупка')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name='Товар')
    quantity = models.PositiveIntegerField(verbose_name='Количество товара')
    price = models.DecimalField(max_digits=19, decimal_places=2, verbose_name='Стоимость товара за 1 единицу/штуку')

    class Meta:
        verbose_name = "Список товаров"
        verbose_name_plural = "Списки товаров"
