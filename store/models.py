from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import os


def get_file_path(instance, filename):
    original_filename = filename
    nowTime = timezone.now().strftime('%Y%m%d%H%M%S')
    filename = "%s%s" % (nowTime, original_filename)
    return os.path.join('uploads/', filename)


class Category(models.Model):
    slug = models.SlugField(max_length=150, unique=True)
    name = models.CharField(max_length=150)
    image = models.ImageField(upload_to=get_file_path, null=True, blank=True)
    description = models.TextField(max_length=500)
    status = models.BooleanField(
        default=False, help_text="0=default, 1=Hidden")
    trending = models.BooleanField(
        default=False, help_text="0=default, 1=Trending")
    meta_title = models.CharField(max_length=150)
    meta_keywords = models.CharField(max_length=150)
    meta_description = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=150, unique=True)
    name = models.CharField(max_length=150)
    product_image = models.ImageField(
        upload_to=get_file_path, null=True, blank=True)
    small_description = models.CharField(max_length=250)
    quantity = models.PositiveIntegerField()
    description = models.TextField(max_length=500)
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.BooleanField(
        default=False, help_text="0=default, 1=Hidden")
    trending = models.BooleanField(
        default=False, help_text="0=default, 1=Trending")
    tag = models.CharField(max_length=150)
    meta_title = models.CharField(max_length=150)
    meta_keywords = models.CharField(max_length=150)
    meta_description = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_qty = models.IntegerField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)


class Order(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)
    fname = models.CharField(max_length=150, null=False)
    Lname = models.CharField(max_length=150, null=False)
    email = models.CharField(max_length=150, null=False)
    phone = models.CharField(max_length=150, null=False)
    address = models.TextField(null=False)
    city = models.CharField(max_length=150, null=False)
    state = models.CharField(max_length=150, null=False)
    country = models.CharField(max_length=150, null=False)
    postalcode = models.CharField(max_length=150, null=False)
    total_price = models.FloatField(null=False)
    payment_id = models.CharField(max_length=250, null=True)
    orderstatuses = (
        ('Pending', 'Pending'),
        ('Out For Shipping', 'Out For Shipping'),
        ('Completed', 'Completed'),
    )
    status = models.CharField(
        max_length=150, choices=orderstatuses, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.FloatField(null=False)
    quantity = models.IntegerField(null=False)

    def __str__(self):
        return f"{self.product.name} - Qty: {self.quantity}"


class ChatBot(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="GeminiUser", null=True
    )
    text_input = models.CharField(max_length=500)
    gemini_output = models.TextField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.text_input
