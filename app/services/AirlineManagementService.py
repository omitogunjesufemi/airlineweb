from typing import List

from app.dto.SelectAircraftDto import SelectAircraftDto
from app.repositories.AircraftRepository import AircraftRepository
from app.dto.AircraftDto import *
from abc import abstractmethod, ABCMeta


class AirlineManagementService(metaclass=ABCMeta):
    @abstractmethod
    def register_aircraft(self, model: RegisterAircraftDto):
        """Register Aircraft Object"""
        raise NotImplementedError

    @abstractmethod
    def edit_aircraft(self, aircraft_id: int, model: EditAircraftDto):
        """Edit Aircraft Object"""
        raise NotImplementedError

    @abstractmethod
    def list_aircraft(self) -> List[ListAircraftDto]:
        """List Aircraft Objects"""
        raise NotImplementedError

    @abstractmethod
    def aircraft_details(self, aircraft_id: int) -> AircraftDetailsDto:
        """Return Aircraft Details"""
        raise NotImplementedError

    @abstractmethod
    def get_all_for_selected_list(self) -> [SelectAircraftDto]:
        """Select Aircraft Object"""
        raise NotImplementedError


class DefaultAirlineManagementService(AirlineManagementService):
    repository: AircraftRepository

    def __init__(self, repository: AircraftRepository):
        self.repository = repository

    def register_aircraft(self, model: RegisterAircraftDto):
        return self.repository.register_aircraft(model)

    def edit_aircraft(self, aircraft_id: int, model: EditAircraftDto):
        return self.repository.edit_aircraft(aircraft_id, model)

    def list_aircraft(self) -> List[ListAircraftDto]:
        return self.repository.list_aircraft()

    def aircraft_details(self, aircraft_id: int) -> AircraftDetailsDto:
        return self.repository.aircraft_details(aircraft_id)

    def delete_aircraft(self, aircraft_id):
        return self.repository.delete_aircraft(aircraft_id)

    def get_all_for_selected_list(self) -> [SelectAircraftDto]:
        return self.repository.get_all_for_selected_list()

