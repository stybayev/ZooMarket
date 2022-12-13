# Generated by Django 4.0.1 on 2022-12-13 14:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0015_remove_user_is_deleted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pet',
            name='pet_type',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='pet', to='authentication.pettype', verbose_name='Вид питомца'),
        ),
    ]