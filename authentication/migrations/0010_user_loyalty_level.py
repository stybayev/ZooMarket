# Generated by Django 4.0.1 on 2022-12-09 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0009_user_add_pet_status_user_pets_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='loyalty_level',
            field=models.PositiveIntegerField(default=1, verbose_name='Уровень лояльности'),
            preserve_default=False,
        ),
    ]
