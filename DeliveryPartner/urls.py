from django.urls import path
from .views import *

urlpatterns = [
    path('', DeliveryDashboard, name='DeliveryDashboard'),
    path('login/', DeliveryLogin, name='DeliveryPartnerLogin'),
    path('logout/', DeliveryLogout, name='DeliveryPartnerLogout'),
    path('verfyOtp/<str:id>/', VerifyOtp, name='VerifyOtp'),
]