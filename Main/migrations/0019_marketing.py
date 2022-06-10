# Generated by Django 3.2.13 on 2022-06-10 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0018_auto_20220610_0858'),
    ]

    operations = [
        migrations.CreateModel(
            name='Marketing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_segment', models.CharField(choices=[('Bon client', 'Bon client'), ('Nouvelle inscription', 'Nouvelle inscription'), ('Client ponctuel', 'Client ponctuel')], max_length=255, null=True)),
                ('description', models.CharField(max_length=255, null=True)),
                ('start_date', models.DateTimeField(null=True)),
                ('end_date', models.DateTimeField(null=True)),
            ],
        ),
    ]