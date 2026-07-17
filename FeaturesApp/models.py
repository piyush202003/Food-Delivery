from django.db import models
from accounts.models import Address
from django.conf import settings
# Create your models here.

class Category(models.Model):
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="categories/")

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='ProductCategory')
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="products/")
    unit = models.CharField(max_length=20)
    stock = models.IntegerField()
    is_organic = models.BooleanField(default=False)
    rating = models.FloatField(default=0)
    review_count = models.IntegerField(default=0)
    discount = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="CartUser")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="CartProduct")
    quantity = models.PositiveIntegerField(default=1)

class DeliveryPartner(models.Model):
    VEHICLE_TYPES = [
        ("bike", "Bike"),
        ("scooter", "Scooter"),
        ("car", "Car"),
    ]
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    avatar = models.ImageField(upload_to="deliveryPartner/")
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_TYPES)
    is_active = models.BooleanField(default=True)

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="OrderUser")
    shipping_address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name="OrderAddress")
    payment_method = models.CharField(max_length=30)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=30)
    delivery_partenr = models.ForeignKey(DeliveryPartner, on_delete=models.CASCADE, null=True, blank=True, related_name="OrderDeliveryPartner")
    delivery_otp = models.CharField(max_length=6)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="OrderItemProduct")
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

class OrderStatus(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="history")
    status = models.CharField(max_length=30)
    timestamp = models.DateTimeField(auto_now_add=True)
    note = models.TextField(blank=True)