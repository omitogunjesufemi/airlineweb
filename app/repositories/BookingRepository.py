from abc import ABCMeta, abstractmethod
from typing import List
from app.models import Booking
from app.dto.BookingDto import *


class BookingRepository(metaclass=ABCMeta):
    @abstractmethod
    def register_booking(self, model: RegisterBookingDto):
        """Booking a Flight for a Passenger"""
        raise NotImplementedError

    @abstractmethod
    def edit_booking(self, booking_id: int, model: EditBookingDto):
        """Edit a booking"""
        raise NotImplementedError

    @abstractmethod
    def list_booking(self) -> List[ListBookingDto]:
        """List of Bookings"""
        raise NotImplementedError

    @abstractmethod
    def booking_details(self, booking_id: int) -> BookingDetailsDto:
        """Details of Booking"""
        raise NotImplementedError

    @abstractmethod
    def delete_booking(self, booking_id: int):
        """Delete a Booking"""
        raise NotImplementedError

    @abstractmethod
    def get_all_bookings(self) -> List[GetBookingDto]:
        """List of Bookings"""
        raise NotImplementedError

    @abstractmethod
    def get_all_flight_id_only(self):
        """Flight_id Only"""
        raise NotImplementedError


class DjangoORMBookingRepository(BookingRepository):
    def register_booking(self, model: RegisterBookingDto):
        booking = Booking()
        booking.flight_id = model.flight_id
        booking.passenger_id = model.passenger_id
        booking.booking_reference = model.booking_reference
        booking.price = model.price
        booking.seat_number = model.seat_number
        booking.flight_class = model.flight_class
        booking.save()
        return booking.id

    def edit_booking(self, booking_id: int, model: EditBookingDto):
        try:
            booking = Booking.objects.get(id=booking_id)
            booking.price = model.price
            booking.flight_class = model.flight_class
            booking.save()
        except Booking.DoesNotExist as e:
            raise e

    def list_booking(self) -> List[ListBookingDto]:
        bookings = list(Booking.objects.values('id',
                                               'flight_id',
                                               'passenger_id',
                                               'booking_reference',
                                               'price',
                                               'flight_class'))
        result: List[ListBookingDto] = []
        for booking in bookings:
            item = ListBookingDto()
            item.booking_reference = booking['booking_reference']
            item.flight_class = booking['flight_class']
            item.price = booking['price']
            item.passenger_id = booking['passenger_id']
            item.flight_id = booking['flight_id']
            item.id = booking['id']
            result.append(item)
        return result

    def booking_details(self, booking_id: int) -> BookingDetailsDto:
        try:
            booking = Booking.objects.get(id=booking_id)
            result = GetBookingDto()
            result.flight_id = booking.flight_id
            result.passenger_id = booking.passenger_id
            result.flight_class = booking.flight_class
            result.booking_reference = booking.booking_reference
            result.seat_number = booking.seat_number
            result.price = booking.price
            result.id = booking_id
            return result
        except Booking.DoesNotExist as e:
            raise e

    def delete_booking(self, booking_id: int):
        try:
            Booking.objects.get(id=booking_id).delete()
        except Booking.DoesNotExist as e:
            raise e

    def get_all_bookings(self) -> List[GetBookingDto]:
        bookings = list(Booking.objects.values('id',
                                               'flight__flight_number',
                                               'flight_id',
                                               'passenger_id',
                                               'flight__take_off_location',
                                               'flight__departure_date',
                                               'flight__destination',
                                               'passenger__user__first_name',
                                               'passenger__user__last_name',
                                               'passenger__user__username',
                                               'passenger__user__email',
                                               'passenger__phone',
                                               'booking_reference',
                                               'seat_number',
                                               'price',
                                               'flight_class'))
        record: List[GetBookingDto] = []
        for booking in bookings:
            item = GetBookingDto()
            item.booking_reference = booking['booking_reference']
            item.seat_number = booking['seat_number']
            item.flight_class = booking['flight_class']
            item.price = booking['price']
            item.first_name = booking['passenger__user__first_name']
            item.last_name = booking['passenger__user__last_name']
            item.username = booking['passenger__user__username']
            item.email = booking['passenger__user__email']
            item.phone = booking['passenger__phone']
            item.flight_number = booking['flight__flight_number']
            item.take_off_location = booking['flight__take_off_location']
            item.departure_date = booking['flight__departure_date']
            item.destination = booking['flight__destination']
            item.passenger_id = booking['passenger_id']
            item.flight_id = booking['flight_id']
            item.id = booking['id']
            # item.save()
            record.append(item)
        return record

    def get_all_flight_id_only(self):
        bookings = list(Booking.objects.values('flight_id'))
        record = []
        for booking in bookings:
            flight_id = booking['flight_id']
            record.append(flight_id)
        return record
