# Generated by Django 5.1.5 on 2025-02-06 15:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_productimage'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ProductImage',
        ),
    ]
