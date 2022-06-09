# Generated by Django 3.2.13 on 2022-06-08 03:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
                ('description', models.CharField(max_length=200, null=True)),
                ('category', models.CharField(choices=[('PC', 'PC'), ('Autre', 'Autre')], max_length=200, null=True)),
                ('n_lot', models.CharField(max_length=200, null=True)),
                ('price_total_HT', models.FloatField(null=True)),
                ('price_total_TTC', models.FloatField(null=True)),
                ('commercial_margin', models.FloatField(null=True)),
                ('stock_q', models.IntegerField(null=True)),
                ('stock_security', models.IntegerField(null=True)),
                ('stock_status', models.CharField(choices=[('Okay', 'Okay'), ('A réapprovisionner', 'A réapprovisionner')], max_length=255, null=True)),
            ],
        ),
    ]