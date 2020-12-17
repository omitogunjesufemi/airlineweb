import json
import uuid
from typing import List

from django.contrib.auth.decorators import login_required
from django.urls import reverse

from app.dto.PassengerDto import RegisterPassengerDto, EditPassengerDto
from app.services.BookingManagementService import BookingManagementService
from app.models import Booking, Passenger
from app.dto.BookingDto import *
from app.service_provider import airline_service_provider
from django.http import HttpResponse, HttpRequest
from django.shortcuts import redirect, render
from app.decorators import allowed_users


@login_required(redirect_field_name='next')
@allowed_users(['passengers'])
def register_booking(request, flight_id):
    flights = airline_service_provider.flight_management_service().flight_details(flight_id=flight_id)
    flight_price = __get_flight_price(flight_id)
    user_id = request.user.id
    passenger = airline_service_provider.passenger_management_service().passengers_details(user_id)
    context = {
        'title': 'Fill in your details',
        'flights': flights,
        'flight_id': flight_id,
        'flight_price': flight_price,
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'email': request.user.email,
        'phone': passenger.phone,
        'address': passenger.address,
        'registration_number': passenger.registration_number,
        'passenger_id': passenger.id,
        'booking_id': ''
    }
    __create_if_post_method(request, context)
    if request.method == 'POST' and context['saved']:
        booking_id = context['booking_id']
        return redirect('booking_details', booking_id)
    return render(request, 'booking/register_booking.html', context)


@login_required(login_url='login')
@allowed_users(['passengers'])
def edit_booking(request, booking_id):
    booking = airline_service_provider.booking_management_service().booking_details(booking_id)
    price = booking.price
    flight_id = booking.flight_id
    passenger_id = booking.passenger_id
    user_id = request.user.id
    passenger = airline_service_provider.passenger_management_service().passengers_details(user_id=user_id)

    context = {
        'title': 'Make your changes',
        'booking': booking,
        'passenger': passenger,
        'price': price,
    }

    new_booking = __edit_if_post_method(request, context, flight_id, booking_id)
    new_passenger = __edit_if_post(request, passenger_id, user_id, context)
    if new_booking is not None and new_passenger is not None:
        context['booking'] = new_booking
        context['passenger'] = new_passenger
        return redirect('passenger_booking_list')
    return render(request, 'booking/edit_booking.html', context)


@login_required(login_url='login')
def list_booking(request):
    bookings = airline_service_provider.booking_management_service().get_all_bookings()
    context = {
        'bookings': bookings,
    }
    return render(request, 'booking/list_booking.html', context)


# @login_required(login_url='login')
# @allowed_users(['passenger'])
def passenger_booking_list(request):
    context = {
        'bookings': 'Nothing'
    }
    __particular_user_booking(request, context)
    return render(request, 'booking/passenger_booking.html', context)


@login_required(login_url='login')
@allowed_users(['passengers'])
def booking_details(request, booking_id):
    booking = __get_booking_or_raise_error(booking_id)
    flight = airline_service_provider.flight_management_service().flight_details(booking.flight_id)
    passenger = Passenger.objects.get(id=booking.passenger_id)

    context = {
        'booking': booking,
        'flight': flight,
        'passenger': passenger,
    }

    return render(request, 'booking/booking_details.html', context)


@login_required(login_url='login')
@allowed_users(['passengers'])
def delete_booking(request, booking_id):
    try:
        airline_service_provider.booking_management_service().delete_booking(booking_id)
        return redirect('index')
    except Booking.DoesNotExist as e:
        raise e


# ASSIGNING SEAT NUMBER
def __seat_number_generator(request, flight_id, count):
    flights = airline_service_provider.flight_management_service().flight_details(flight_id=flight_id)
    aircraft_id = flights.aircraft_id
    aircraft = airline_service_provider.aircraft_management_service().aircraft_details(aircraft_id)
    capacity = aircraft.capacity
    if count <= capacity:
        seat_number = count
        return seat_number
    elif count > capacity:
        raise Exception


def __set_seat_if_flight_id_exist(flight_id):
    bookings = airline_service_provider.booking_management_service().get_all_flight_id_only()
    count = 1
    for flight in bookings:
        if flight_id == flight:
            count += 1
    return count


# MAKING A BOOKING
def __get_booking_attribute(request, register_booking_dto, context):
    register_booking_dto.passenger_id = context['passenger_id']
    register_booking_dto.flight_class = request.POST['flight_class']


def __set_booking_attribute(request: HttpRequest, context):
    register_booking_dto = RegisterBookingDto()
    register_booking_dto.flight_id = context['flight_id']
    register_booking_dto.flight_class = request.POST['flight_class']
    __get_booking_attribute(request, register_booking_dto, context)
    return register_booking_dto


def __create_if_post_method(request, context):
    if request.method == 'POST':
        try:
            booking = __set_booking_attribute(request, context)
            booking.booking_reference = str(uuid.uuid4()).replace('-', '')[0:10].upper()
            booking.price = __flight_class_and_price(booking.flight_class, booking.flight_id)
            count = __set_seat_if_flight_id_exist(booking.flight_id)
            booking.seat_number = __seat_number_generator(request, booking.flight_id, count)
            booking_id = airline_service_provider.booking_management_service().register_booking(booking)
            context['saved'] = 'success'
            context['booking_id'] = booking_id
            return context
        except Exception as e:
            context['saved'] = 'error'
            raise e


def __get_flight_price(flight_id):
    flights = airline_service_provider.flight_management_service().flight_details(flight_id=flight_id)
    flight_price = flights.price
    return flight_price


def __flight_class_and_price(flight_class, flight_id):
    flights = airline_service_provider.flight_management_service().flight_details(flight_id=flight_id)
    flight_price = flights.price
    if flight_class == 'First':
        flight_price = float(flight_price) * 2
        return flight_price

    elif flight_class == 'Business':
        flight_price = float(flight_price) * 1.5
        return flight_price

    elif flight_class == 'Economic':
        return flight_price


def __get_booking_or_raise_error(booking_id):
    try:
        booking = airline_service_provider.booking_management_service().booking_details(booking_id)
        return booking
    except Exception as e:
        raise e


# EDITING A BOOKING
def __get_booking_attribute_edit(request, edit_booking_dto):
    edit_booking_dto.flight_class = request.POST['flight_class']



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


def __set_booking_attribute_edit(request):
    edit_booking_dto = EditBookingDto()
    edit_booking_dto.flight_class = request.POST['flight_class']
    __get_booking_attribute_edit(request, edit_booking_dto)
    return edit_booking_dto


def __edit_if_post_method(request, context, flight_id, booking_id):
    if request.method == 'POST':
        try:
            booking = __set_booking_attribute_edit(request)
            booking.price = __flight_class_and_price(booking.flight_class, flight_id)
            airline_service_provider.booking_management_service().edit_booking(booking_id, booking)
            context['saved'] = 'success'
            return __get_booking_or_raise_error(booking_id)
        except Booking.DoesNotExist as e:
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


# LISTING BOOKINGS FOR A PARTICULAR PASSENGER
def __particular_user_booking(request, context):
    user_id = request.user.id
    passenger = airline_service_provider.passenger_management_service().passengers_details(user_id)
    passenger_id = passenger.id

    try:
        bookings = airline_service_provider.booking_management_service().get_all_bookings()
        booking_list: List[GetBookingDto] = []

        for booking in bookings:
            if passenger_id == booking.passenger_id:
                booking_list.append(booking)

        context['bookings'] = booking_list
    except Booking.DoesNotExist as e:
        raise e
