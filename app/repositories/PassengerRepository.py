from abc import ABCMeta, abstractmethod

from django.contrib.auth.models import User, Group

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
        passenger.address = model.address
        passenger.phone = model.phone
        passenger.registration_number = model.registration_number

        user = User.objects.create_user(username=model.username, email=model.email, password=model.password)
        user.first_name = model.first_name
        user.last_name = model.last_name

        user.save()

        passenger.user = user

        passengers = Group.objects.get(name__exact='passengers')
        user.groups.add(passengers)

        passenger.save()
        return passenger.id

    def edit_passenger(self, passenger_id: int, model: EditPassengerDto):
        try:
            passenger = Passenger.objects.get(id=passenger_id)
            passenger.user.first_name = model.first_name
            passenger.user.last_name = model.last_name
            passenger.user.email = model.email
            passenger.user.username = model.username
            passenger.address = model.address
            # passenger.date_updated = model.date_updated
            passenger.save()
        except Passenger.DoesNotExist as e:
            print('This Passenger does not exist!')
            raise e

    def list_passenger(self) -> List[ListPassengerDto]:
        passengers = list(Passenger.objects.values('id',
                                                   'user__first_name',
                                                   'user__last_name',
                                                   'user__email',
                                                   'user__username',
                                                   'address',
                                                   'phone',
                                                   'registration_number'))
        results: List[ListPassengerDto] = []
        for passenger in passengers:
            item = ListPassengerDto()
            item.id = passenger['id']
            item.first_name = passenger['user__first_name']
            item.last_name = passenger['user__last_name']
            item.username = passenger['user__username']
            item.address = passenger['address']
            item.phone = passenger['phone']
            item.email = passenger['user__email']
            item.registration_number = passenger['registration_number']
            # item.date_created = passenger['date_created']
            # item.date_updated = passenger['date_updated']
            results.append(item)
        return results

    def passengers_details(self, passenger_id: int) -> PassengerDetailsDto:
        passenger = Passenger.objects.get(id=passenger_id)
        result = PassengerDetailsDto()
        result.first_name = passenger.user.first_name
        result.last_name = passenger.user.last_name
        result.phone = passenger.phone
        result.address = passenger.address
        result.email = passenger.user.email
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
