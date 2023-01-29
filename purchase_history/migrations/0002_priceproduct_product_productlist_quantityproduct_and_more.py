# Generated by Django 4.0.1 on 2023-01-29 09:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('purchase_history', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PriceProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=19, null=True, verbose_name='Стоимость товара за 1 единицу/штуку')),
                ('price_date', models.DateField(blank=True, null=True, verbose_name='Дата добавления цены')),
                ('created_at', models.DateField(auto_now=True, verbose_name='Дата создания цены')),
            ],
            options={
                'verbose_name': '03 Стоимость товара за 1 единицу/штуку',
                'verbose_name_plural': '03 Стоимости товаров за 1 единицу/штуку',
                'ordering': ['price_date'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vendor_code', models.CharField(blank=True, max_length=255, null=True, verbose_name='Артикул товара')),
                ('title', models.CharField(blank=True, max_length=255, null=True, verbose_name='Название товара')),
                ('brand', models.CharField(blank=True, max_length=255, null=True, verbose_name='Производитель/Бренд товара')),
                ('created_at', models.DateField(auto_now=True, verbose_name='Дата товара')),
            ],
            options={
                'verbose_name': '01 Описание товара',
                'verbose_name_plural': '01 Описания товаров',
                'ordering': ['brand'],
            },
        ),
        migrations.CreateModel(
            name='ProductList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField(auto_now=True, verbose_name='Дата создания списка товара')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_list', to=settings.AUTH_USER_MODEL, verbose_name='Покупатель')),
            ],
            options={
                'verbose_name': '02 Список товаров',
                'verbose_name_plural': '02 Список товаров',
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='QuantityProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity_product', models.PositiveIntegerField(verbose_name='Количества товаров')),
                ('created_at', models.DateField(auto_now=True, verbose_name='Дата добавления количества')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quantity_product', to='purchase_history.product', verbose_name='Товар')),
                ('product_list', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='quantity_product', to='purchase_history.productlist', verbose_name='Список товаров')),
            ],
            options={
                'verbose_name': '04 Количество товара',
                'verbose_name_plural': '04 Количества товаров',
                'ordering': ['created_at'],
            },
        ),
        migrations.DeleteModel(
            name='ProductDescription',
        ),
        migrations.AddField(
            model_name='product',
            name='product_list',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_descriptions', to='purchase_history.productlist', verbose_name='Список товаров'),
        ),
        migrations.AddField(
            model_name='priceproduct',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prices', to='purchase_history.product', verbose_name='Товар'),
        ),
    ]
