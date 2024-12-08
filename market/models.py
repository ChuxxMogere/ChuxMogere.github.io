
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser

from django.db import models


# Create your models here.
class User(AbstractUser):
    is_buyer = models.BooleanField('Is buyer', default=False)
    is_farmer = models.BooleanField('Is farmer', default=False)
    photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)


User = get_user_model()


class Product(models.Model):
    DoesNotExist = None
    objects = None
    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="product_images/")
    farmer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.name



class Cart(models.Model):
    objects = None
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.user.username}'s cart - {self.product.name}"

    @property
    def total_price(self):
        return self.quantity * self.product.price

class Order(models.Model):
    objects = None
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_option = models.CharField(max_length=100)
    status = models.CharField(max_length=50, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order by {self.user.username} - {self.status}"

class OrderItem(models.Model):
    objects = None
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} - {self.quantity} x {self.price}"

class Notification(models.Model):
    objects = None
    farmer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.farmer.username} - {self.message}"




