# Generated by Django 3.2.13 on 2022-06-10 02:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0011_auto_20220609_1551'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='name',
        ),
    ]