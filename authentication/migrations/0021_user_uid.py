# Generated by Django 4.0.1 on 2023-01-18 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0020_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='uid',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
