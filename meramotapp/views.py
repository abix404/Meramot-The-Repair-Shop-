from django.contrib.auth.models import User
import random
from .models import Category, Service, Booking, SellerProfile, CustomUser
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import SellerSignUpForm, SellerProfileForm, UserSignupForm, ServiceForm, BookingForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.


def home(request):
    categories = Category.objects.all()

    all_services = list(Service.objects.all())  # Fetch all services
    random_services = random.sample(all_services, min(len(all_services), 10))  # Pick 10 random
    initial_services = random_services[:5]  # First 5 services for the slider

    return render(request, "home.html", {
        "categories": categories,
        "services": random_services,
        "initial_services": initial_services,
    })

# Category

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category_list.html', {'categories': categories})


def search_services(request):
    query = request.GET.get('query', '')
    results = Service.objects.filter(title__icontains=query) if query else []
    return render(request, 'search_results.html', {'results': results, 'query': query})



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


# Logout
def user_logout(request):
    logout(request)
    return redirect("home")


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


@login_required
def seller_dashboard(request):
    services = Service.objects.filter(seller=request.user)
    return render(request, 'seller/seller_dashboard.html', {'services': services})

@login_required
def add_service(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            service = form.save(commit=False)
            service.seller = request.user  # Assign logged-in seller
            service.save()
            return redirect('seller_dashboard')
    else:
        form = ServiceForm()
    return render(request, 'seller/add_service.html', {'form': form})

@login_required
def edit_service(request, service_id):
    service = get_object_or_404(Service, id=service_id, seller=request.user)
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            form.save()
            return redirect('seller_dashboard')
    else:
        form = ServiceForm(instance=service)
    return render(request, 'seller/edit_service.html', {'form': form})

@login_required
def delete_service(request, service_id):
    service = get_object_or_404(Service, id=service_id, seller=request.user)
    if request.method == 'POST':
        service.delete()
        return redirect('seller_dashboard')
    return render(request, 'seller/delete_service.html', {'service': service})


def service_detail(request, pk):
    service = get_object_or_404(Service, id=pk)
    return render(request, "service_detail.html", {"service": service})


@login_required
def book_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)

    if request.user.is_seller:
            return redirect("home")

    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.service = service
            booking.save()
            return redirect('booking_success' ,booking_id=booking.id)
    else:
        form = BookingForm()

    return render(request, 'booking.html', {'service': service, 'form': form})

@login_required
def booking_success(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    return render(request, 'booking_success.html', {'booking': booking})


@login_required
def user_dashboard(request):
    if request.user.is_seller:
        return redirect("seller_dashboard")  # Prevent sellers from accessing

    orders = Booking.objects.filter(user=request.user)
    completed_services = Service.objects.filter(booking__user=request.user, booking__status="Completed")

    return render(request, "user/user_dashboard.html", {"orders": orders, "completed_services": completed_services})

@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Booking, id=order_id, user=request.user)

    if order.status == "Pending":  # Ensure only pending orders can be canceled
        order.status = "Canceled"
        order.save()
        messages.success(request, "Your order has been canceled successfully.")
    else:
        messages.error(request, "You can only cancel pending orders.")

    return redirect("user_dashboard")

def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.is_seller:
                return redirect("seller/seller_dashboard")
            else:
                return redirect("user/user_dashboard")
        else:
            return render(request, "auth/login.html", {"error": "Invalid credentials"})

    return render(request, "auth/login.html")

