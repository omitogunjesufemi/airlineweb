import datetime
import uuid

from django.http import HttpResponse, Http404, HttpRequest

from app.dto.AircraftDto import *
from app.models import Aircraft
from app.service_provider import airline_service_provider
from django.shortcuts import redirect, render
from django.http.request import HttpRequest


def register_aircraft(request):
    context = {

    }
    __create_if_post_method(request, context)
    if request.method == 'POST' and context['saved']:
        return redirect('list_aircraft')
    return render(request, 'aircraft/register_aircraft.html', context)


def edit_aircraft(request, aircraft_id):
    edit_aircraft_dto = __get_aircraft_details_or_raise_404(request, aircraft_id)
    context = {
        'aircraft': edit_aircraft_dto
    }
    new_edit_aircraft = __edit_if_post_method(request, aircraft_id, context)
    if new_edit_aircraft is not None:
        context['aircraft'] = new_edit_aircraft
        return redirect('list_aircraft')
    return render(request, 'aircraft/edit_aircraft.html/', context)


def delete_aircraft(request, aircraft_id):
    airline_service_provider.aircraft_management_service().delete_aircraft(aircraft_id)
    return redirect('list_aircraft')


def list_aircraft(request):
    aircrafts = airline_service_provider.aircraft_management_service().list_aircraft()
    context = {
        'title': 'List Aircraft',
        'aircrafts': aircrafts
    }
    return render(request, 'aircraft/list_aircraft.html', context)


def aircraft_details(request, aircraft_id: int):
    aircraft = __get_aircraft_details_or_raise_404(request, aircraft_id)
    context = {
        'aircraft': aircraft
    }
    return render(request, 'aircraft/aircraft_details.html', context)


def __get_aircraft_details_or_raise_404(request, aircraft_id: int):
    try:
        aircraft = airline_service_provider.aircraft_management_service().aircraft_details(aircraft_id)
        return aircraft
    except Aircraft.DoesNotExist:
        raise Http404('Aircraft does not exist!')


def __get_aircraft_attribute_from_request_edit(edit_aircraft_dto, request):
    edit_aircraft_dto.aircraft_name = request.POST['aircraft_name']
    edit_aircraft_dto.aircraft_type = request.POST['aircraft_type']
    edit_aircraft_dto.capacity = request.POST['capacity']


def __set_aircraft_attribute_from_request_edit(request, aircraft_id: int):
    edit_aircraft_dto = EditAircraftDto()
    edit_aircraft_dto.id = aircraft_id
    __get_aircraft_attribute_from_request_edit(edit_aircraft_dto, request)
    return edit_aircraft_dto


def __get_aircraft_attribute_from_request(register_aircraft_dto, request):
    register_aircraft_dto.aircraft_name = request.POST['aircraft_name']
    register_aircraft_dto.aircraft_type = request.POST['aircraft_type']
    register_aircraft_dto.capacity = request.POST['capacity']


def __set_aircraft_attribute_from_request(request: HttpRequest):
    register_aircraft_dto = RegisterAircraftDto()
    register_aircraft_dto.aircraft_name = request.POST['aircraft_name']
    __get_aircraft_attribute_from_request(register_aircraft_dto, request)
    return register_aircraft_dto


def __create_if_post_method(request, context):
    try:
        if request.method == 'POST':
            aircraft = __set_aircraft_attribute_from_request(request)
            aircraft.date_created = datetime.date.today()
            aircraft.aircraft_number = str(uuid.uuid4()).replace('-', '')[0:10].upper()
            airline_service_provider.aircraft_management_service().register_aircraft(aircraft)
            # return 'ok'
            context['saved'] = 'success'
        return context
    except Exception as e:
        print(e)
        context['saved'] = 'error'


def __edit_if_post_method(request, aircraft_id: int, context):
    if request.method == 'POST':
        try:
            aircraft = __set_aircraft_attribute_from_request_edit(request, aircraft_id)
            aircraft.date_updated = datetime.date.today()
            airline_service_provider.aircraft_management_service().edit_aircraft(aircraft_id, aircraft)
            context['saved'] = 'success'
            return __get_aircraft_details_or_raise_404(request, aircraft_id)
        except Exception as e:
            print(e)
            context['saved'] = 'error'

