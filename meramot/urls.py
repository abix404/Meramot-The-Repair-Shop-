"""
URL configuration for meramot project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from meramotapp import views as views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.home, name='home'),

    path("seller/seller_signup/", views.seller_signup, name="seller_signup"),

    path("login/",  LoginView.as_view(template_name="auth/login.html"), name="login"),

    path("logout/", LogoutView.as_view(next_page="/"), name="logout"),

    path("signup/", views.user_signup, name="user_signup"),

    path("user/user-dashboard/", views.user_dashboard,  name="user_dashboard"),

    path("cancel-order/<int:order_id>/", views.cancel_order, name="cancel_order"),

    path('seller/seller-dashboard/', views.seller_dashboard, name='seller_dashboard'),

    path('seller/add-service/', views.add_service, name='add_service'),

    path('seller/edit-service/<int:service_id>/', views.edit_service, name='edit_service'),

    path('seller/delete-service/<int:service_id>/', views.delete_service, name='delete_service'),

    path('categories/', views.category_list, name='category_list'),

    path('search/', views.search_services, name='search_services'),

    path('service/<int:pk>/', views.service_detail, name='service_detail'),

    path('book/<int:service_id>/', views.book_service, name='book_service'),

    path('booking/success/<int:booking_id>/', views.booking_success, name='booking_success'),

    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),

    path("verify-seller/<int:seller_id>/", views.verify_seller, name="verify_seller"),

    path("manage-orders/", views.manage_orders, name="manage_orders"),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
