from abc import ABCMeta, abstractmethod
from typing import List
from app.repositories.BookingRepository import BookingRepository
from app.dto.BookingDto import *


class BookingManagementService(metaclass=ABCMeta):
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
    def get_all_bookings(self) -> List[ListBookingDto]:
        """List of Bookings"""
        raise NotImplementedError

    def get_all_flight_id_only(self):
        """Flight_id Only"""
        raise NotImplementedError

    @abstractmethod
    def booking_details(self, booking_id: int) -> BookingDetailsDto:
        """Details of Booking"""
        raise NotImplementedError

    @abstractmethod
    def delete_booking(self, booking_id: int):
        """Delete a Booking"""
        raise NotImplementedError


class DefaultBookingManagementService(BookingManagementService):
    repository: BookingRepository

    def __init__(self, repository: BookingRepository):
        self.repository = repository

    def register_booking(self, model: RegisterBookingDto):
        return self.repository.register_booking(model)

    def edit_booking(self, booking_id: int, model: EditBookingDto):
        return self.repository.edit_booking(booking_id, model)

    def list_booking(self) -> List[ListBookingDto]:
        return self.repository.list_booking()

    def get_all_bookings(self) -> List[ListBookingDto]:
        return self.repository.get_all_bookings()

    def get_all_flight_id_only(self):
        return self.repository.get_all_flight_id_only()

    def booking_details(self, booking_id: int) -> BookingDetailsDto:
        return self.repository.booking_details(booking_id)

    def delete_booking(self, booking_id: int):
        return self.repository.delete_booking(booking_id)
