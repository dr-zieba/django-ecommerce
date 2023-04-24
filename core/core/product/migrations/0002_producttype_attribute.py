# Generated by Django 4.1.5 on 2023-04-24 18:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("product", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="producttype",
            name="attribute",
            field=models.ManyToManyField(
                related_name="product_type_attribute",
                through="product.ProductTypeAttribute",
                to="product.attribute",
            ),
        ),
    ]
