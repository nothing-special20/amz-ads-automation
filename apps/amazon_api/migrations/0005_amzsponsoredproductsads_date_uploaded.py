# Generated by Django 3.2.13 on 2022-07-17 00:02

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('amazon_api', '0004_amzsponsoredproductsads'),
    ]

    operations = [
        migrations.AddField(
            model_name='amzsponsoredproductsads',
            name='DATE_UPLOADED',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
