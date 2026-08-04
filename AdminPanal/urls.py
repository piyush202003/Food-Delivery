from django.urls import path
from .views import *

urlpatterns = [
    path('', AdminDashboard, name='AdminDashboard'),
    path('products/', AdminProducts, name='AdminProducts'),
    path('products/new/', AdminProductForm, name='AdminProductForm'),
    path('products/<str:id>/edit/', AdminProductForm, name='AdminProductFormEdit'),
    path('orders/', AdminOrders, name='AdminOrders'),
    path('delivery-partners/', AdminDeliveryPartners, name='AdminDeliveryPartners'),
    path('logout/', AdminLogout, name='AdminLogout'),    
]