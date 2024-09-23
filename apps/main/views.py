import json
from django.http import JsonResponse
from datetime import date, timedelta
from django.db.models.functions import ExtractYear
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, FloatField, F
from django.db.models.functions import Coalesce
from django.shortcuts import render
from django.db.models import Min, Max

from apps.products.models import Product, Category
from apps.sales.models import Sale

from apps.authentication.decorators import (
    admin_or_manager_required,
    admin_required,
    admin_or_manager_or_staff_required,
)


# =================================== Home User view  ===================================
def index(request):
    products = Product.objects.prefetch_related("images", "productvolume_set").filter(
        status="ACTIVE"
    )

    products_with_images = []
    for product in products:
        images = product.images.filter(is_default=True)
        if not images.exists():
            images = product.images.all()

        volumes = product.productvolume_set.all()
        if volumes.exists():
            min_price = volumes.aggregate(Min("price"))["price__min"]
            max_price = volumes.aggregate(Max("price"))["price__max"]
        else:
            min_price = max_price = None

        products_with_images.append(
            {
                "product": product,
                "images": images,
                "min_price": min_price,
                "max_price": max_price,
            }
        )

    return render(
        request,
        "index.html",
        {
            "products_with_images": products_with_images,
            "user": request.user,
        },
    )


@login_required
@admin_or_manager_or_staff_required
def get_total_sales_for_period(start_date, end_date):
    return (
        Sale.objects.filter(trans_date__range=[start_date, end_date]).aggregate(
            total_sales=Sum("grand_total")
        )["total_sales"]
        or 0
    )


# =================================== The dashboard view ===================================
@login_required
@admin_or_manager_or_staff_required
def dashboard(request):
    today = date.today()
    year = today.year

    # Calculate monthly earnings
    monthly_earnings = [
        Sale.objects.filter(trans_date__year=year, trans_date__month=month).aggregate(
            total=Coalesce(Sum("grand_total"), 0.0)
        )["total"]
        for month in range(1, 13)
    ]

    # Calculate annual earnings
    annual_earnings = Sale.objects.filter(trans_date__year=year).aggregate(
        total=Coalesce(Sum("grand_total"), 0.0)
    )["total"]
    annual_earnings = format(annual_earnings, ".2f")

    # Average monthly earnings
    avg_month = format(sum(monthly_earnings) / 12, ".2f")

    # Total sales for today, week, and month
    def get_total_sales_for_period(start_date, end_date):
        return (
            Sale.objects.filter(trans_date__range=[start_date, end_date]).aggregate(
                total_sales=Coalesce(Sum("grand_total"), 0.0)
            )["total_sales"]
            or 0
        )

    total_sales_today = get_total_sales_for_period(today, today)
    start_of_week = today - timedelta(days=today.weekday())
    total_sales_week = get_total_sales_for_period(start_of_week, today)
    start_of_month = today.replace(day=1)
    total_sales_month = get_total_sales_for_period(start_of_month, today)

    # Top-selling products
    top_products = Product.objects.annotate(
        quantity_sum=Sum("inventory__quantity")
    ).order_by("-quantity_sum")[:3]

    top_products_data = [
        (p.name, p.inventory.quantity if hasattr(p, "inventory") else 0)
        for p in top_products
    ]
    top_products_data += [("None", 0)] * (3 - len(top_products_data))

    top_products_names = [name for name, _ in top_products_data]
    top_products_quantity = [quantity for _, quantity in top_products_data]

    # Total stock from Inventory
    total_stock = Product.objects.filter(status="ACTIVE").aggregate(
        total=Coalesce(Sum("inventory__quantity"), 0)
    )["total"]

    context = {
        "active_icon": "dashboard",
        "products": Product.objects.filter(status="ACTIVE").count(),
        "total_stock": total_stock,
        "categories": Category.objects.count(),
        "annual_earnings": annual_earnings,
        "monthly_earnings": json.dumps(monthly_earnings),
        "avg_month": avg_month,
        "total_sales_today": total_sales_today,
        "total_sales_week": total_sales_week,
        "total_sales_month": total_sales_month,
        "top_products_names": json.dumps(top_products_names),
        "top_products_quantity": json.dumps(top_products_quantity),
    }

    return render(request, "main/dashboard.html", context)


@login_required
@admin_or_manager_or_staff_required
def monthly_earnings_view(request):
    today = date.today()
    year = today.year
    monthly_earnings = []

    for month in range(1, 13):
        earning = (
            Sale.objects.filter(trans_date__year=year, trans_date__month=month)
            .aggregate(
                total_variable=Coalesce(
                    Sum(F("grand_total")), 0.0, output_field=FloatField()
                )
            )
            .get("total_variable")
        )
        monthly_earnings.append(earning)

    return JsonResponse(
        {
            "labels": [
                "Jan",
                "Feb",
                "Mar",
                "Apr",
                "May",
                "Jun",
                "Jul",
                "Aug",
                "Sep",
                "Oct",
                "Nov",
                "Dec",
            ],
            "data": monthly_earnings,
        }
    )


# =================================== Annual Sales graph ===================================
@login_required
@admin_or_manager_or_staff_required
def sales_data_api(request):
    # Query to get total sales grouped by year
    sales_per_year = (
        Sale.objects.annotate(year=ExtractYear("trans_date"))
        .values("year")
        .annotate(total_sales=Sum("grand_total"))
        .order_by("year")
    )

    # Prepare the data as a dictionary
    data = {
        "years": [item["year"] for item in sales_per_year],
        "total_sales": [item["total_sales"] for item in sales_per_year],
    }

    # Return the data as JSON
    return JsonResponse(data)