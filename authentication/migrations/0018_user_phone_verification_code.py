# Generated by Django 4.0.1 on 2022-12-21 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0017_user_phone_verified'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='phone_verification_code',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]