from abc import ABCMeta, abstractmethod
from app.models import Aircraft
from typing import List

from app.dto.AircraftDto import AircraftDetailsDto, EditAircraftDto, ListAircraftDto, RegisterAircraftDto
from app.dto.SelectAircraftDto import SelectAircraftDto


class AircraftRepository(metaclass=ABCMeta):
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
    def delete_aircraft(self, aircraft_id: int):
        """Delete Aircraft Details"""
        raise NotImplementedError

    @abstractmethod
    def get_all_for_selected_list(self) -> [SelectAircraftDto]:
        """Select Aircraft Object"""
        raise NotImplementedError


class DjangoORMAircraftRepository(AircraftRepository):
    def register_aircraft(self, model: RegisterAircraftDto):
        aircraft = Aircraft()
        aircraft.aircraft_capacity = model.capacity
        aircraft.aircraft_type = model.aircraft_type
        aircraft.aircraft_no = model.aircraft_number
        aircraft.aircraft_name = model.aircraft_name
        aircraft.date_created = model.date_created
        aircraft.save()

    def edit_aircraft(self, aircraft_id: int, model: EditAircraftDto):
        try:
            aircraft = Aircraft.objects.get(id=aircraft_id)
            aircraft.aircraft_capacity = model.capacity
            aircraft.aircraft_type = model.aircraft_type
            aircraft.aircraft_name = model.aircraft_name
            aircraft.date_updated = model.date_updated
            aircraft.save()
        except Aircraft.DoesNotExist as e:
            message = 'Aircraft does not exist'
            print(message)
            raise e

    def list_aircraft(self) -> List[ListAircraftDto]:
        aircraft = list(Aircraft.objects.values('id', 'aircraft_name', 'aircraft_type', 'aircraft_no',
                                                'aircraft_capacity', 'date_created', 'date_updated'))
        results: List[ListAircraftDto] = []
        for air in aircraft:
            item = ListAircraftDto()
            item.id = air['id']
            item.aircraft_type = air['aircraft_type']
            item.aircraft_name = air['aircraft_name']
            item.aircraft_number = air['aircraft_no']
            item.capacity = air['aircraft_capacity']
            item.date_created = air['date_created']
            item.date_updated = air['date_updated']
            results.append(item)
        return results

    def aircraft_details(self, aircraft_id: int) -> AircraftDetailsDto:
        aircraft = Aircraft.objects.get(id=aircraft_id)
        result = AircraftDetailsDto()
        result.aircraft_name = aircraft.aircraft_name
        result.aircraft_number = aircraft.aircraft_no
        result.capacity = aircraft.aircraft_capacity
        result.aircraft_type = aircraft.aircraft_type
        result.date_created = aircraft.date_created
        result.date_updated = aircraft.date_updated
        result.id = aircraft_id
        return result

    def delete_aircraft(self, aircraft_id: int):
        try:
            Aircraft.objects.get(id=aircraft_id).delete()
        except Aircraft.DoesNotExist:
            print("Aircraft Does Not Exist")

    def get_all_for_selected_list(self) -> [SelectAircraftDto]:
        aircrafts = list(Aircraft.objects.values('id', 'aircraft_name'))
        result: List[SelectAircraftDto] = []
        for aircraft in aircrafts:
            item = SelectAircraftDto()
            item.id = aircraft['id']
            item.aircraft_name = aircraft['aircraft_name']
            result.append(item)
        return result
