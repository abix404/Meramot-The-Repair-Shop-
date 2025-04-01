from django.contrib.auth.models import User
from .models import Category, Service, SellerProfile, CustomUser
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import SellerSignUpForm, SellerProfileForm, UserSignupForm, ServiceForm
from django.contrib import messages



# Create your views here.


def home(request):
    categories = Category.objects.all()
    top_services = Service.objects.order_by('-rating')[:4]  # Show top 4 services

    return render(request, 'home.html', {'categories': categories, 'top_services': top_services})

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






