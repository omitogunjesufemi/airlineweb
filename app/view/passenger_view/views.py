import datetime
import json
import uuid

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404, HttpRequest
from django.urls import reverse

from app.dto.PassengerDto import *
from app.models import Passenger
from app.service_provider import airline_service_provider
from django.shortcuts import redirect, render
from django.http.request import HttpRequest


# REGISTER HERE
def register_passenger(request):
    if request.user.has_perm('app.add_passenger'):
        context = {
            'title': 'Fill in Your Details'
        }
        passenger = __create_if_post(request, context)
        if request.method == 'POST' and context['saved']:
            username = passenger.username
            password = passenger.password
            user: User = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.groups.filter(name__exact='passengers').exists():
                    nex = request.session.get('next')
                    print(nex)
                    return redirect(nex)
            return redirect('')
        return render(request, 'passenger/register_passenger.html', context)
    else:
        context = {
            'message': 'You are not authorised for this view'
        }
        return render(request, 'error_message.html', context)


# EDIT HERE
def edit_passenger(request, passenger_id):
    if request.user.has_perm('app.change_passenger'):
        editing_passenger_object = __get_passenger_details_or_raise_error(passenger_id)
        context = {
            'passenger': editing_passenger_object,
            'title': 'Change your Details'
        }
        new_editing_passenger_object = __edit_if_post(request, passenger_id, context)
        if new_editing_passenger_object is not None:
            context['passenger'] = new_editing_passenger_object
            return redirect('list_passenger')
        return render(request, 'passenger/edit_passenger.html', context)
    else:
        context = {
            'message': 'You are authorised!'
        }
        return render(request, 'error_message.html', context)


# DELETE HERE
def delete_passenger(request, passenger_id):
    if request.user.has_perm('app.delete_passenger'):
        airline_service_provider.passenger_management_service().delete_passenger(passenger_id)
        return redirect('list_passenger')
    else:
        context = {
            'message': 'You are not authorised'
        }


# LIST HERE
def list_passenger(request):
    if request.user.has_perm('app.view_passenger'):
        passengers = airline_service_provider.passenger_management_service().list_passenger()
        context = {
            'title': 'List of Passengers',
            'passengers': passengers
        }
        return render(request, 'passenger/list_passenger.html', context)
    else:
        context = {
            'message': 'You are not authorised'
        }
        return render(request, 'error_message.html', context)


# PASSENGER DETAILS HERE
def passenger_details(request, passenger_id):
    if request.user.has_perm('app.view_passenger'):
        passenger = __get_passenger_details_or_raise_error(passenger_id)
        context = {
            'passenger': passenger,
        }
        return render(request, 'passenger/passenger_details.html', context)
    else:
        context = {
            'message': 'You are not authorised'
        }
        return render(request, 'error_message.html', context)

# REGISTERING A PASSENGER
def __set_passenger_attribute_request(request: HttpRequest):
    register_passenger_dto = RegisterPassengerDto()
    register_passenger_dto.first_name = request.POST['first_name']
    __get_passenger_attribute_request(register_passenger_dto, request)
    return register_passenger_dto


def __get_passenger_attribute_request(register_passenger_dto, request):
    register_passenger_dto.last_name = request.POST['last_name']
    register_passenger_dto.phone = request.POST['phone']
    register_passenger_dto.email = request.POST['email']
    register_passenger_dto.address = request.POST['address']
    register_passenger_dto.confirm_password = request.POST['confirm_password']
    register_passenger_dto.password = request.POST['password']
    register_passenger_dto.username = request.POST['username']


def __create_if_post(request, context):
    if request.method == 'POST':
        try:
            passenger = __set_passenger_attribute_request(request)
            password = passenger.password
            confirm = passenger.confirm_password
            if password == confirm:
                passenger.registration_number = str(uuid.uuid4()).replace('-', '')[0:10].upper()
                airline_service_provider.passenger_management_service().register_passenger(passenger)
                context['saved'] = 'success'
                context['message'] = 'saved'
                return passenger
            else:
                context['saved'] = False
        except Exception as e:
            print(e)
            context['saved'] = 'error'


# EDITING A PASSENGER
def __get_passenger_attribute_edit(request, edit_passenger_dto):
    edit_passenger_dto.first_name = request.POST['first_name']
    edit_passenger_dto.last_name = request.POST['last_name']
    edit_passenger_dto.username = request.POST['username']
    edit_passenger_dto.phone = request.POST['phone']
    edit_passenger_dto.email = request.POST['email']
    edit_passenger_dto.address = request.POST['address']


def __set_passenger_attribute_edit(request, passenger_id):
    edit_passenger_dto = EditPassengerDto()
    edit_passenger_dto.id = passenger_id
    edit_passenger_dto.first_name = request.POST['first_name']
    __get_passenger_attribute_edit(request, edit_passenger_dto)
    return edit_passenger_dto


def __get_passenger_details_or_raise_error(passenger_id):
    try:
        result = airline_service_provider.passenger_management_service().passengers_details(passenger_id)
        return result
    except Passenger.DoesNotExist as e:
        print('Not Found')
        raise e


def __edit_if_post(request, passenger_id, user_id, context):
    if request.method == 'POST':
        try:
            passenger = __set_passenger_attribute_edit(request, user_id)
            airline_service_provider.passenger_management_service().edit_passenger(passenger_id, passenger)
            context['saved'] = 'success'
            return airline_service_provider.passenger_management_service().passengers_details(user_id)
        except Passenger.DoesNotExist as e:
            print('Cannot Edit a Passenger that does not exist!')
            raise e
