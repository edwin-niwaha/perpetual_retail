# Generated by Django 4.2.16 on 2024-11-18 17:26

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="productimage",
            name="image",
            field=cloudinary.models.CloudinaryField(
                blank=True, max_length=255, null=True, verbose_name="image"
            ),
        ),
    ]
