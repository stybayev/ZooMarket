# Generated by Django 4.0.1 on 2023-02-06 13:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('purchase_history', '0007_productlist_product'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productlist',
            old_name='product',
            new_name='products',
        ),
    ]
