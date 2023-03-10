# Generated by Django 4.1.3 on 2022-12-11 15:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0005_alter_product_price"),
    ]

    operations = [
        migrations.CreateModel(
            name="ProductDetails",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("brand_name", models.CharField(max_length=100)),
                ("title", models.CharField(max_length=100)),
                ("description", models.CharField(max_length=200)),
                (
                    "product",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="product_details",
                        to="store.product",
                    ),
                ),
            ],
        ),
    ]
