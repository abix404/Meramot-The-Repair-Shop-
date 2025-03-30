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


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.home, name='home'),

    path("seller/signup/", views.seller_signup, name="seller_signup"),

    path("dashboard/", views.seller_dashboard, name="seller_dashboard"),

    path("update/", views.seller_update, name="seller_update"),

    path("delete/", views.seller_delete, name="seller_delete"),

    path("logout/", views.user_logout, name="logout"),

    path("login/", views.user_login, name="login"),

    path("signup/", views.user_signup, name="user_signup"),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
