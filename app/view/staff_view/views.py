from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http.request import HttpRequest
from app.service_provider import airline_service_provider
from app.decorators import allowed_users


@login_required(login_url='login')
@allowed_users(['staffs'])
def list_staff(request):
    staffs = airline_service_provider.staff_management_service().list_staff()
    context = {
        'staffs': staffs,
    }
    return render(request, '', context)


@login_required(login_url='login')
@allowed_users(['staffs'])
def staff_home(request):
    context = {
        'welcome': "Welcome to the Staff HomePage!",
    }
    return render(request, 'staff/staff_home.html', context)