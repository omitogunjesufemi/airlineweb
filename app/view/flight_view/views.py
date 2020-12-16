import datetime
import uuid

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404, HttpRequest

from app.decorators import allowed_users
from app.dto.FlightDto import *
from app.models import Flight
from django.shortcuts import redirect, render
from django.http.request import HttpRequest
from app.service_provider import airline_service_provider
from typing import List


@login_required(login_url='login')
@allowed_users(['staffs'])
def register_flight(request):
    aircrafts = airline_service_provider.aircraft_management_service().get_all_for_selected_list()
    context = {
        'aircrafts': aircrafts
    }
    __create_if_post_method(request, context)
    if request.method == 'POST' and context['saved']:
        return redirect('list_flight')
    return render(request, 'flight/register_flight.html', context)


@login_required(login_url='login')
@allowed_users(['staffs'])
def edit_flight(request, flight_id: int):
    aircrafts = airline_service_provider.aircraft_management_service().get_all_for_selected_list()
    editing_flight = __get_flight_or_raise_error(flight_id)
    context = {
        'flight': editing_flight,
        'arrival_time': editing_flight.arrival_time.strftime("%H:%M"),
        'departure_date': editing_flight.departure_date.strftime("%Y-%m-%d"),
        'aircrafts': aircrafts
    }
    new_editing_flight = __edit_if_post(request, flight_id, context)
    if new_editing_flight is not None:
        context['flight'] = new_editing_flight
        return redirect('list_flight')
    return render(request, 'flight/edit_flight.html', context)


@login_required(login_url='login')
@allowed_users(['staffs'])
def list_flight(request):
    flights = airline_service_provider.flight_management_service().list_flight()
    context = {
        'title': 'List Flight',
        'flights': flights
    }
    return render(request, 'flight/list_flight.html', context)


@login_required(login_url='login')
@allowed_users(['staffs'])
def flight_details(request, flight_id: int):
    flight = __get_flight_or_raise_error(flight_id)
    context = {
        'flight': flight
    }
    return render(request, 'flight/flight_details.html', context)


@login_required(login_url='login')
@allowed_users(['staffs'])
def delete_flight(request, flight_id: int):
    airline_service_provider.flight_management_service().delete_flight(flight_id)
    return redirect('list_flight')


# REGISTERING A FLIGHT
def __get_register_flight_attribute(register_dto, request):
    register_dto.take_off_location = request.POST['take_off_location']
    register_dto.price = request.POST['price']
    register_dto.arrival_time = request.POST['arrival_time']
    register_dto.destination = request.POST['destination']
    register_dto.departure_date = request.POST['departure_date']


def __set_register_flight_attribute(request: HttpRequest):
    register_dto = RegisterFlightDto()
    register_dto.aircraft_id = request.POST['aircraft_id']
    __get_register_flight_attribute(register_dto, request)
    return register_dto


def __create_if_post_method(request, context):
    try:
        if request.method == 'POST':
            flight = __set_register_flight_attribute(request)
            flight.date_created = datetime.date.today()
            flight.flight_number = str(uuid.uuid4()).replace('-', '')[0:10].upper()
            airline_service_provider.flight_management_service().register_flight(flight)
            context['saved'] = 'success'
        return context
    except Exception as e:
        print(e)
        context['saved'] = 'error'


# EDITING FLIGHT
def __get_flight_attribute_edit(edit_flight_dto, request):
    edit_flight_dto.aircraft_id = request.POST['aircraft_id']
    edit_flight_dto.take_off_location = request.POST['take_off_location']
    edit_flight_dto.price = request.POST['price']
    edit_flight_dto.arrival_time = request.POST['arrival_time']
    edit_flight_dto.destination = request.POST['destination']
    edit_flight_dto.departure_date = request.POST['departure_date']


def __set_flight_attribute_edit(request, flight_id):
    edit_flight_dto = EditFlightDto()
    edit_flight_dto.id = flight_id
    __get_flight_attribute_edit(edit_flight_dto, request)
    return edit_flight_dto


def __get_flight_or_raise_error(flight_id):
    try:
        result = airline_service_provider.flight_management_service().flight_details(flight_id)
        return result
    except Flight.DoesNotExist as e:
        print('This Flight does not exist!')
        raise e


def __edit_if_post(request, flight_id: int, context):
    if request.method == 'POST':
        try:
            flight = __set_flight_attribute_edit(request, flight_id)
            flight.date_updated = datetime.date.today()
            airline_service_provider.flight_management_service().edit_flight(flight_id, flight)
            context['saved'] = 'success'
            return __get_flight_or_raise_error(flight_id)
        except Exception as e:
            context['saved'] = 'error'
            raise e
