# Generated by Django 4.0.1 on 2022-12-09 13:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0011_alter_user_add_pet_status_alter_user_loyalty_level_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='pets',
        ),
        migrations.AddField(
            model_name='pet',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='pet', to=settings.AUTH_USER_MODEL, verbose_name='Владелец питомца'),
        ),
    ]
