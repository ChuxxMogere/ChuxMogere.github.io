# Generated by Django 5.1.3 on 2024-11-30 16:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0006_remove_product_farmer_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='timestamp',
        ),
    ]