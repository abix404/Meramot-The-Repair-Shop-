from django.db import models
from django.contrib.auth.models import AbstractUser, User, Group, Permission
from django.conf import settings
# Create your models here.


# -------------------------------
# 1️⃣ Custom User Model
# -------------------------------
class CustomUser(AbstractUser):

    is_seller = models.BooleanField(default=False) # To check if user is a seller
    mobile_no = models.CharField(max_length=15, unique=True, null=True, blank=True)
    groups = models.ManyToManyField(Group, related_name="customuser_set", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="customuser_permissions", blank=True)

    def __str__(self):
        return self.username
# -------------------------------
# 1️⃣ Custom Seller Model
# -------------------------------
class SellerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    mobile_no = models.CharField(max_length=15, unique=True)
    address = models.TextField()
    experience = models.CharField(max_length=255)
    image = models.ImageField(upload_to='sellers/', default='default.jpg')
    approved = models.BooleanField(default=False)  # Admin Approval Required

    def __str__(self):
        return self.user.username

# -------------------------------
# 2️⃣ Category Model
# -------------------------------
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='category_images/', null=True, blank=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


# -------------------------------
# 3️⃣ Service Model (Offered by Sellers)
# -------------------------------
class Service(models.Model):
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'is_seller': True})
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='service_images/', null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    rating = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.seller.username}"


# -------------------------------
# 4️⃣ Booking Model
# -------------------------------
class Booking(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    date = models.DateField()
    time_slot = models.CharField(max_length=50)  # Example: "10:00 AM - 11:00 AM"
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled')
    ], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.service.title} ({self.date} {self.time_slot})"
# -------------------------------
# 6️⃣ Cart
# -------------------------------

# -------------------------------
# 5️⃣ Order Model (For Cart & Checkout)
# -------------------------------
class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled')
    ], default='pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.user.username}"


# -------------------------------
# 6️⃣ Review & Rating Model
# -------------------------------
class Review(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(default=5)  # Rating out of 5
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.service.title} ({self.rating} ⭐)"
