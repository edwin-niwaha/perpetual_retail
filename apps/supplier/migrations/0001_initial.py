# Generated by Django 4.2.16 on 2024-10-31 21:28

from django.db import migrations, models
import django.utils.timezone
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Supplier",
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
                (
                    "name",
                    models.CharField(max_length=255, verbose_name="Supplier Name"),
                ),
                (
                    "contact_name",
                    models.CharField(max_length=255, verbose_name="Contact Name"),
                ),
                (
                    "email",
                    models.EmailField(max_length=254, verbose_name="Email Address"),
                ),
                (
                    "phone",
                    phonenumber_field.modelfields.PhoneNumberField(
                        blank=True,
                        default="+12125552368",
                        max_length=128,
                        null=True,
                        region=None,
                        verbose_name="Telephone",
                    ),
                ),
                ("address", models.CharField(max_length=255, verbose_name="Address")),
                (
                    "created_at",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="Created At"
                    ),
                ),
            ],
        ),
    ]
