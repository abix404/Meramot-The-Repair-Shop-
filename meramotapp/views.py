import random
from meramotapp.models import CustomUser,User, Category, Service, Booking, SellerProfile, Order
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import SellerProfileForm, UserSignupForm, ServiceForm, BookingForm, SellerSignUpForm, UserLoginForm
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

def category_services(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    services = Service.objects.filter(category=category)
    return render(request, "category_services.html", {"category": category, "services": services})

def search_services(request):
    query = request.GET.get('query', '')
    results = Service.objects.filter(title__icontains=query) if query else []
    return render(request, 'search_results.html', {'results': results, 'query': query})



# Seller Registration
def seller_signup(request):
    if request.method == "POST":
        form = SellerSignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_seller = True  # Mark as seller
            user.is_normal_user = False  # Ensure they are not a normal user
            user.save()
            messages.success(request, "Seller account created! You can now log in.")

            return redirect("login")  # Redirect to login page
        else:
            messages.error(request, "Something went wrong. Please check your inputs.")
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

# General User Sign Up

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

# Seller Activities
@login_required
def seller_dashboard(request):
        services = Service.objects.filter(seller=request.user)
        return render(request, "seller/seller_dashboard.html", {"services": services})

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

# General User Activities
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
        return redirect("seller_dashboard")

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

# General User Login
def user_login(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)

                if user.is_seller:
                    return redirect("seller/seller_dashboard")
                else:
                    return redirect("user/user_dashboard")
            else:
                messages.error(request, "Invalid username or password.")

    return render(request, "auth/login.html", {"form": form})

# Admin Activities
def is_admin(user):
    return user.is_superuser

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    users = CustomUser.objects.all()
    sellers = CustomUser.objects.filter(is_seller=True, is_active=False)  # Pending verification
    orders = Order.objects.all()
    return render(request, "admin/admin_dashboard.html", {"users": users, "sellers": sellers, "orders": orders})

@login_required
@user_passes_test(is_admin)
def verify_seller(request, seller_id):
    seller = get_object_or_404(CustomUser, id=seller_id)
    seller.is_active = True
    seller.save()
    messages.success(request, "Seller has been verified.")
    return redirect("admin_dashboard")

@user_passes_test(is_admin)
def admin_manage_booking(request):
    bookings = Booking.objects.all().order_by('-created_at')
    return render(request, "admin/admin_manage_booking.html", {"bookings": bookings})

@user_passes_test(is_admin)
def update_booking_status(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if request.method == "POST":
        new_status = request.POST.get("status")
        booking.status = new_status
        booking.save()
        return redirect("admin_manage_booking")
    return redirect("admin_manage_booking")



