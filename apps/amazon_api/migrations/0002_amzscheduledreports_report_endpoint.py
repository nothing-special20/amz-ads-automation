# Generated by Django 3.2.13 on 2022-07-01 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('amazon_api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='amzscheduledreports',
            name='REPORT_ENDPOINT',
            field=models.TextField(default='_'),
        ),
    ]
