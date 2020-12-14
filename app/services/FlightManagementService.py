from abc import ABCMeta, abstractmethod
from typing import List
from app.dto.SelectAircraftDto import SelectFlightDto
from app.repositories.FlightRepository import FlightRepository
from app.dto.FlightDto import *


class FlightManagementService(metaclass=ABCMeta):
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


class DefaultFlightManagementService(FlightManagementService):
    repository: FlightRepository

    def __init__(self, repository: FlightRepository):
        self.repository = repository

    def register_flight(self, model: RegisterFlightDto):
        return self.repository.register_flight(model)

    def edit_flight(self, flight_id: int, model: EditFlightDto):
        return self.repository.edit_flight(flight_id, model)

    def list_flight(self) -> List[ListFlightDto]:
        return self.repository.list_flight()

    def flight_details(self, flight_id: int) -> FlightDetailDto:
        return self.repository.flight_details(flight_id)

    def delete_flight(self, flight_id: int):
        return self.repository.delete_flight(flight_id)

    def get_all_for_selected_list(self) -> [SelectFlightDto]:
        return self.repository.get_all_for_selected_list()
