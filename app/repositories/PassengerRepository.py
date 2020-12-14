from abc import ABCMeta, abstractmethod
from app.dto.PassengerDto import *
from typing import List
from app.models import Passenger


class PassengerRepository(metaclass=ABCMeta):
    @abstractmethod
    def register_passenger(self, model: RegisterPassengerDto):
        """Register Passenger Object"""
        raise NotImplementedError

    @abstractmethod
    def edit_passenger(self, passenger_id: int, model: EditPassengerDto):
        """Edit Passenger Object"""
        raise NotImplementedError

    @abstractmethod
    def list_passenger(self) -> List[ListPassengerDto]:
        """List Passenger Object"""
        raise NotImplementedError

    @abstractmethod
    def passengers_details(self, passenger_id: int) -> PassengerDetailsDto:
        """Details of Passenger Object"""
        raise NotImplementedError

    @abstractmethod
    def delete_passenger(self, passenger_id: int):
        """Delete Passenger Object"""
        raise NotImplementedError


class DjangoORMPassengerRepository(PassengerRepository):
    def register_passenger(self, model: RegisterPassengerDto):
        passenger = Passenger()
        passenger.last_name = model.last_name
        passenger.first_name = model.first_name
        passenger.address = model.address
        passenger.phone = model.phone
        passenger.email = model.email
        passenger.registration_number = model.registration_number
        passenger.save()
        return passenger.id

    def edit_passenger(self, passenger_id: int, model: EditPassengerDto):
        try:
            passenger = Passenger.objects.get(id=passenger_id)
            passenger.first_name = model.first_name
            passenger.last_name = model.last_name
            passenger.address = model.address
            # passenger.date_updated = model.date_updated
            passenger.save()
        except Passenger.DoesNotExist as e:
            print('This Passenger does not exist!')
            raise e

    def list_passenger(self) -> List[ListPassengerDto]:
        passengers = list(Passenger.objects.values('id', 'first_name', 'last_name', 'address',
                                                   'phone', 'email', 'registration_number'))
        results: List[ListPassengerDto] = []
        for passenger in passengers:
            item = ListPassengerDto()
            item.id = passenger['id']
            item.first_name = passenger['first_name']
            item.last_name = passenger['last_name']
            item.address = passenger['address']
            item.phone = passenger['phone']
            item.email = passenger['email']
            item.registration_number = passenger['registration_number']
            # item.date_created = passenger['date_created']
            # item.date_updated = passenger['date_updated']
            results.append(item)
        return results

    def passengers_details(self, passenger_id: int) -> PassengerDetailsDto:
        passenger = Passenger.objects.get(id=passenger_id)
        result = PassengerDetailsDto()
        result.first_name = passenger.first_name
        result.last_name = passenger.last_name
        result.phone = passenger.phone
        result.address = passenger.address
        result.email = passenger.email
        result.registration_number = passenger.registration_number
        # result.date_updated = passenger.date_updated
        # result.date_created = passenger.date_created
        result.id = passenger_id
        return result

    def delete_passenger(self, passenger_id):
        try:
            Passenger.objects.get(id=passenger_id).delete()
        except Passenger.DoesNotExist as e:
            print('Not Found')
            raise e
