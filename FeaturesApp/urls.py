from django.urls import path
from .views import *

urlpatterns = [
    path("", Home, name = "Home"),
    path("products/", Products, name="Products"),
    path("products/<str:pdid>/", ProductPage, name = "ProductPage"),
    path("search/", SearchResults, name="SearchResults"),
    path("deals/", FlashDeals, name = "FlashDeals"),
    path("checkout/", Checkout, name="Checkout"),
    path("orders/", MyOrders, name="MyOrders"),
    path("orders/<int:odid>/", OrderTracking, name = "OrderTracking"),
    path("addresses/", Addresses, name = "Addresses"),
    path("cart/add/<str:product_id>/", add_to_cart, name="AddToCart"),
]