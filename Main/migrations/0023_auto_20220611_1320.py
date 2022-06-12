# Generated by Django 3.2.13 on 2022-06-11 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0022_alter_order_satisfaction_score'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='satisfaction_score',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('en préparation', 'en préparation'), ('expédié', 'expédié'), ('livré', 'livré'), ('retour client', 'retour client')], default='livré', max_length=255, null=True),
        ),
    ]