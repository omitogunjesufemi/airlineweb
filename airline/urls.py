"""airline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include
from app.view.index_view import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('aircraft/', include('app.view.aircraft_view.urls')),
    path('flight/', include('app.view.flight_view.urls')),
    path('passenger/', include('app.view.passenger_view.urls')),
    path('booking/', include('app.view.booking_view.urls')),
    path('login/', include('app.view.login_view.urls')),
    path('password/', include('app.view.password_change.urls')),
    path('staff/', include('app.view.staff_view.urls')),
]
