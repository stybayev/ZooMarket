# Generated by Django 4.0.1 on 2023-02-06 13:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('purchase_history', '0005_alter_product_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='product_list',
        ),
        migrations.RemoveField(
            model_name='productlist',
            name='user',
        ),
        migrations.RemoveField(
            model_name='quantityproduct',
            name='product_list',
        ),
    ]