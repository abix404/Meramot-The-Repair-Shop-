from .models import Category, Service, SellerProfile, CustomUser
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import SellerSignUpForm, SellerProfileForm, UserSignupForm
from django.contrib import messages
from django.contrib.auth.models import User



# Create your views here.


def home(request):
    categories = Category.objects.all()
    top_services = Service.objects.order_by('-rating')[:4]  # Show top 4 services

    return render(request, 'home.html', {'categories': categories, 'top_services': top_services})

# Seller Registration
def seller_signup(request):
    if request.method == "POST":
        form = SellerSignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("seller_dashboard")
    else:
        form = SellerSignUpForm()
    return render(request, "seller/seller_signup.html", {"form": form})

# Seller Dashboard
@login_required
def seller_dashboard(request):
    seller = get_object_or_404(SellerProfile, user=request.user)
    return render(request, "seller/seller_dashboard.html", {"seller": seller})

# Update Seller Profile
@login_required
def seller_update(request):
    seller = get_object_or_404(SellerProfile, user=request.user)
    if request.method == "POST":
        form = SellerProfileForm(request.POST, request.FILES, instance=seller)
        if form.is_valid():
            form.save()
            return redirect("seller_dashboard")
    else:
        form = SellerProfileForm(instance=seller)
    return render(request, "seller/seller_update.html", {"form": form})

# Delete Seller Profile
@login_required
def seller_delete(request):
    seller = get_object_or_404(SellerProfile, user=request.user)
    if request.method == "POST":
        request.user.delete()
        return redirect("home")
    return render(request, "seller/seller_delete.html")

# Logout
def user_logout(request):
    logout(request)
    return redirect("home")

def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.is_seller:  # If the user is a seller
                return redirect("seller_dashboard")  # Redirect to seller dashboard
            else:
                return redirect("home")  # Redirect to normal user homepage
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "auth/login.html")

def register(request):
    if request.method == "POST":
        form = UserSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in the user after registration
            if user.is_seller:
                return redirect("seller_dashboard")  # Redirect seller
            else:
                return redirect("home")  # Redirect normal user
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserSignupForm()

    return render(request, "auth/signup.html", {"form": form})



def user_signup(request):
    if request.method == "POST":
        form = UserSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect("home") 
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserSignupForm()

    return render(request, "auth/signup.html", {"form": form})



