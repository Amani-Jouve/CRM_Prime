# Generated by Django 3.2.13 on 2022-06-10 04:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0014_claim'),
    ]

    operations = [
        migrations.AlterField(
            model_name='claim',
            name='Type',
            field=models.CharField(choices=[('erreur prix', 'erreur prix'), ('article erronné', 'article erronné'), ('article defectueux', 'article defectueux'), ('retard livraison', 'retard livraison')], max_length=255, null=True),
        ),
    ]