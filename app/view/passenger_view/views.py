import datetime
import json
import uuid
from django.http import HttpResponse, Http404, HttpRequest
from django.urls import reverse

from app.dto.PassengerDto import *
from app.models import Passenger
from app.service_provider import airline_service_provider
from django.shortcuts import redirect, render
from django.http.request import HttpRequest


# REGISTER HERE
def register_passenger(request, flight_id):
    flight = airline_service_provider.flight_management_service().flight_details(flight_id)
    context = {
        'title': 'Fill in Your Details',
        'flight': flight
    }
    if request.method == 'GET':
        return render(request, 'passenger/register_passenger.html', context)
    passenger = __set_passenger_attribute_request(request)
    json_data = json.dumps(passenger.__dict__)
    response = HttpResponse(status=302)
    response.set_cookie('flight_id', flight_id)
    response.set_cookie('passenger', json_data)
    response['location'] = reverse('register_booking', args=[flight_id])
    return response


# EDIT HERE
def edit_passenger(request, passenger_id):
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


# DELETE HERE
def delete_passenger(request, passenger_id):
    airline_service_provider.passenger_management_service().delete_passenger(passenger_id)
    return redirect('list_passenger')


# LIST HERE
def list_passenger(request):
    passengers = airline_service_provider.passenger_management_service().list_passenger()
    context = {
        'title': 'List of Passengers',
        'passengers': passengers
    }
    return render(request, 'passenger/list_passenger.html', context)


# PASSENGER DETAILS HERE
def passenger_details(request, passenger_id):
    passenger = __get_passenger_details_or_raise_error(passenger_id)
    context = {
        'passenger': passenger,
    }
    return render(request, 'passenger/passenger_details.html', context)


# REGISTERING A PASSENGER
def __set_passenger_attribute_request(request):
    register_passenger_dto = RegisterPassengerDto()
    register_passenger_dto.first_name = request.POST['first_name']
    register_passenger_dto.registration_number = str(uuid.uuid4()).replace('-', '')[0:10].upper()
    __get_passenger_attribute_request(request, register_passenger_dto)
    return register_passenger_dto


def __get_passenger_attribute_request(request, register_passenger_dto):
    register_passenger_dto.last_name = request.POST['last_name']
    register_passenger_dto.phone = request.POST['phone']
    register_passenger_dto.email = request.POST['email']
    register_passenger_dto.address = request.POST['address']


def __create_if_post(request, context):
    if request.method == 'POST':
        try:
            passenger = __set_passenger_attribute_request(request)
            passenger.registration_number = str(uuid.uuid4()).replace('-', '')[0:10].upper()
            airline_service_provider.passenger_management_service().register_passenger(passenger)
            context['saved'] = 'success'
            return context
        except Exception as e:
            print(e)
            context['saved'] = 'error'


# EDITING A PASSENGER
def __get_passenger_attribute_edit(request, edit_passenger_dto):
    edit_passenger_dto.first_name = request.POST['first_name']
    edit_passenger_dto.last_name = request.POST['last_name']
    edit_passenger_dto.phone = request.POST['phone']
    edit_passenger_dto.email = request.POST['email']
    edit_passenger_dto.address = request.POST['address']


def __set_passenger_attribute_edit(request, passenger_id: int):
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


def __edit_if_post(request, passenger_id, context):
    if request.method == 'POST':
        try:
            passenger = __set_passenger_attribute_edit(request, passenger_id)
            airline_service_provider.passenger_management_service().edit_passenger(passenger_id, passenger)
            context['saved'] = 'success'
            return __get_passenger_details_or_raise_error(passenger_id)
        except Passenger.DoesNotExist as e:
            print('Cannot Edit a Passenger that does not exist!')
            raise e
