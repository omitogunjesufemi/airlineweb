from typing import List
from app.repositories.PassengerRepository import PassengerRepository
from app.dto.PassengerDto import *
from abc import abstractmethod, ABCMeta


class PassengerManagementService(metaclass=ABCMeta):
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
    def passengers_details(self, user_id: int) -> PassengerDetailsDto:
        """Details of Passenger Object"""
        raise NotImplementedError

    @abstractmethod
    def delete_passenger(self, passenger_id: int):
        """Delete Passenger Object"""
        raise NotImplementedError


class DefaultPassengerManagementService(PassengerManagementService):
    repository = PassengerRepository

    def __init__(self, repository: PassengerRepository):
        self.repository = repository

    def register_passenger(self, model: RegisterPassengerDto):
        return self.repository.register_passenger(model)

    def edit_passenger(self, passenger_id: int, model: EditPassengerDto):
        return self.repository.edit_passenger(passenger_id, model)

    def list_passenger(self) -> List[ListPassengerDto]:
        return self.repository.list_passenger()

    def passengers_details(self, user_id: int) -> PassengerDetailsDto:
        return self.repository.passengers_details(user_id)

    def delete_passenger(self, passenger_id: int):
        return self.repository.delete_passenger(passenger_id)