from django.contrib import admin
from .models import CustomUser, Category, Service, Booking, Order, Review
# Register your models here.


admin.site.register(CustomUser)
admin.site.register(Category)
admin.site.register(Service)
admin.site.register(Booking)
admin.site.register(Order)
admin.site.register(Review)
