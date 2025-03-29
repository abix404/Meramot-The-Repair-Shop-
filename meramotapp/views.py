from django.shortcuts import render
from .models import Category, Service


# Create your views here.


def home(request):
    categories = Category.objects.all()
    top_services = Service.objects.order_by('-rating')[:4]  # Show top 4 services

    return render(request, 'home.html', {'categories': categories, 'top_services': top_services})
