from abc import ABCMeta, abstractmethod
from app.models import Flight, Aircraft
from typing import List
from app.dto.SelectAircraftDto import SelectFlightDto
from app.dto.FlightDto import *


class FlightRepository(metaclass=ABCMeta):
    @abstractmethod
    def register_flight(self, model: RegisterFlightDto):
        """Register FLight Object"""
        raise NotImplementedError

    @abstractmethod
    def edit_flight(self, flight_id: int, model: EditFlightDto):
        """Edit Flight Object"""
        raise NotImplementedError

    @abstractmethod
    def list_flight(self) -> List[ListFlightDto]:
        """List FLight Object"""
        raise NotImplementedError

    @abstractmethod
    def flight_details(self, flight_id: int) -> FlightDetailDto:
        """Flight Object Details"""
        raise NotImplementedError

    @abstractmethod
    def delete_flight(self, flight_id: int):
        """Delete Flight Details"""
        raise NotImplementedError

    @abstractmethod
    def get_all_for_selected_list(self) -> [SelectFlightDto]:
        """Select Flight Number"""
        raise NotImplementedError


class DjangoORMFlightRepository(FlightRepository):
    def register_flight(self, model: RegisterFlightDto):
        flight = Flight()
        flight.aircraft_id = model.aircraft_id
        flight.flight_number = model.flight_number
        flight.take_off_location = model.take_off_location
        flight.departure_date = model.departure_date
        flight.destination = model.destination
        flight.arrival_time = model.arrival_time
        flight.price = model.price
        flight.date_created = model.date_created
        flight.save()

    def edit_flight(self, flight_id: int, model: EditFlightDto):
        try:
            flight = Flight.objects.get(id=flight_id)
            flight.aircraft_id = model.aircraft_id
            flight.take_off_location = model.take_off_location
            flight.departure_date = model.departure_date
            flight.destination = model.destination
            flight.price = model.price
            flight.arrival_time = model.arrival_time
            flight.date_updated = model.date_updated
            flight.save()
        except Flight.DoesNotExist as e:
            message = 'Flight does not exist!'
            print(message)
            return e

    def list_flight(self) -> List[ListFlightDto]:
        flights = list(Flight.objects.values('aircraft__aircraft_name', 'flight_number', 'take_off_location',
                                             'departure_date', 'destination', 'arrival_time', 'date_created',
                                             'date_updated', 'price', 'id', 'aircraft_id'))
        results: List[ListFlightDto] = []
        for lit in flights:
            item = ListFlightDto()
            item.aircraft_name = lit['aircraft__aircraft_name']
            item.aircraft_id = lit['aircraft_id']
            item.flight_number = lit['flight_number']
            item.take_off_location = lit['take_off_location']
            item.departure_date = lit['departure_date']
            item.destination = lit['destination']
            item.arrival_time = lit['arrival_time']
            item.date_created = lit['date_created']
            item.date_updated = lit['date_updated']
            item.price = lit['price']
            item.id = lit['id']
            results.append(item)
        return results

    def flight_details(self, flight_id: int) -> FlightDetailDto:
        try:
            flight = Flight.objects.get(id=flight_id)
            result = FlightDetailDto()
            result.aircraft_id = flight.aircraft.id
            result.aircraft_name = flight.aircraft.aircraft_name
            result.arrival_time = flight.arrival_time
            result.destination = flight.destination
            result.price = flight.price
            result.date_created = flight.date_created
            result.date_updated = flight.date_updated
            result.departure_date = flight.departure_date
            result.flight_number = flight.flight_number
            result.take_off_location = flight.take_off_location
            result.id = flight.id
            return result
        except Flight.DoesNotExist as e:
            raise e

    def delete_flight(self, flight_id: int):
        try:
            Flight.objects.get(id=flight_id).delete()
        except Flight.DoesNotExist:
            print("Flight Does Not Exist!")

    def get_all_for_selected_list(self) -> [SelectFlightDto]:
        flights = list(Flight.objects.values('id', 'aircraft__flight__flight_number'))
        results: List[SelectFlightDto] = []
        for flight in flights:
            item = SelectFlightDto()
            item.id = flight['id']
            item.flight_number = flight['aircraft__flight__flight_number']
            results.append(item)
        return results




