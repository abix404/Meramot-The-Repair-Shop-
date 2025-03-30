from django.contrib import admin
from .models import Category, Service, Booking, Order, Review, SellerProfile, CustomUser
from django.contrib.auth.admin import UserAdmin
# Register your models here.

@admin.register(SellerProfile)
class SellerAdmin(admin.ModelAdmin):
    list_display = ("user", "mobile_no", "approved")
    list_editable = ("approved",)


admin.site.register(CustomUser, UserAdmin)
admin.site.register(Category)
admin.site.register(Service)
admin.site.register(Booking)
admin.site.register(Order)
admin.site.register(Review)
