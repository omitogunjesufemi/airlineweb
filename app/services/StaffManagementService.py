from abc import ABCMeta, abstractmethod
from app.repositories.StaffRepository import *


class StaffManagementService(metaclass=ABCMeta):
    @abstractmethod
    def register_staff(self, model: RegisterStaffDto):
        """Register Staff"""
        raise NotImplementedError

    @abstractmethod
    def edit_staff(self, staff_id: int, model: EditStaffDto):
        """Edit Staff"""
        raise NotImplementedError

    @abstractmethod
    def list_staff(self, model: ListStaffDto):
        """List Staff"""
        raise NotImplementedError

    @abstractmethod
    def staff_details(self, staff_id: int) -> StaffDetailsDto:
        """Staff Details"""
        raise NotImplementedError

    @abstractmethod
    def delete_staff(self, staff_id: int):
        """Delete Staff"""
        raise NotImplementedError


class DefaultStaffManagementService(StaffManagementService):
    repository = StaffRepository

    def __init__(self, repository: StaffRepository):
        self.repository = repository

    def register_staff(self, model: RegisterStaffDto):
        return self.repository.register_staff(model)

    def edit_staff(self, staff_id: int, model: EditStaffDto):
        return self.repository.edit_staff(staff_id, model)

    def list_staff(self, model: ListStaffDto):
        return self.repository.list_staff(model)

    def staff_details(self, staff_id: int) -> StaffDetailsDto:
        return self.repository.staff_details(staff_id)

    def delete_staff(self, staff_id: int):
        return self.repository.delete_staff(staff_id)

