# Generated by Django 3.2.13 on 2022-06-10 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0017_alter_customer_dob'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='Delivery_date_expected',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='Delivery_date_final',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
