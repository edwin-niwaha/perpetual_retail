from django.urls import path
from . import views

app_name = "orders"
urlpatterns = [
    path("product/<int:id>/", views.product_detail, name="product_detail"),
    # cart
    path("add-to-cart/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/", views.cart_view, name="cart"),
    path("checkout/", views.checkout_view, name="checkout"),
    path(
        "order-confirmation/<int:order_id>/",
        views.order_confirmation_view,
        name="order_confirmation",
    ),
    # orders
    path(
        "order-history/",
        views.customer_order_history_view,
        name="customer_order_history",
    ),
    path("cashier-orders/", views.cashier_orders_view, name="cashier_orders"),
    path("order/<int:order_id>/", views.order_detail_view, name="order_detail_view"),
    path(
        "to-be-processed/",
        views.orders_to_be_processed_view,
        name="orders_to_be_processed",
    ),
    path("report/<int:order_id>/", views.order_report_view, name="order_report"),
    path("process/<int:order_id>/", views.order_process_view, name="order_process"),
]