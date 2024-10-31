# Generated by Django 4.2.16 on 2024-10-31 21:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ChartOfAccounts",
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
                    "account_name",
                    models.CharField(max_length=255, verbose_name="Account Name"),
                ),
                (
                    "account_type",
                    models.CharField(
                        choices=[
                            ("asset", "Asset"),
                            ("liability", "Liability"),
                            ("equity", "Equity"),
                            ("revenue", "Revenue"),
                            ("expense", "Expense"),
                        ],
                        max_length=50,
                        verbose_name="Account Type",
                    ),
                ),
                (
                    "account_number",
                    models.CharField(
                        max_length=20, unique=True, verbose_name="Account Number"
                    ),
                ),
                (
                    "description",
                    models.TextField(blank=True, null=True, verbose_name="Description"),
                ),
            ],
            options={
                "verbose_name": "Chart of Account",
                "verbose_name_plural": "Chart of Accounts",
                "db_table": "chart_of_accounts",
                "ordering": ["account_number"],
            },
        ),
        migrations.CreateModel(
            name="Transaction",
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
                    "amount",
                    models.DecimalField(
                        decimal_places=2, max_digits=10, verbose_name="Amount"
                    ),
                ),
                (
                    "transaction_type",
                    models.CharField(
                        choices=[("credit", "Credit"), ("debit", "Debit")],
                        max_length=10,
                        verbose_name="Type",
                    ),
                ),
                (
                    "transaction_date",
                    models.DateField(verbose_name="Date of Transaction"),
                ),
                (
                    "description",
                    models.TextField(blank=True, null=True, verbose_name="Narrations"),
                ),
                (
                    "account",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="finance.chartofaccounts",
                        verbose_name="Account",
                    ),
                ),
            ],
        ),
    ]
