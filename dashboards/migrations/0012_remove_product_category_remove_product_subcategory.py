# Generated by Django 4.2.1 on 2023-07-03 13:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboards', '0011_remove_product_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='category',
        ),
        migrations.RemoveField(
            model_name='product',
            name='subcategory',
        ),
    ]