from abc import ABCMeta, abstractmethod
from typing import List

from app.dto.StaffDto import *
from app.models import Staff
from django.contrib.auth.models import User, Group


class StaffRepository(metaclass=ABCMeta):
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
    def staff_details(self, user_id: int) -> StaffDetailsDto:
        """Staff Details"""
        raise NotImplementedError

    @abstractmethod
    def delete_staff(self, staff_id: int):
        """Delete Staff"""
        raise NotImplementedError


class DjangoORMStaffRepository(StaffRepository):
    def register_staff(self, model: RegisterStaffDto):
        staff = Staff()
        staff.department = model.department
        staff.role = model.role
        staff.date_of_employment = model.date_of_employment

        user = User.objects.create_user(username=model.username, email=model.email, password=model.password)
        user.first_name = model.first_name
        user.last_name = model.last_name

        user.save()

        staff.user = user

        staffs = Group.objects.get(name__exact='staffs')
        user.groups.add(staffs)

        staff.save()

    def edit_staff(self, staff_id: int, model: EditStaffDto):
        try:
            staff = Staff.objects.get(id=staff_id)
            staff.role = model.role
            staff.user.first_name = model.first_name
            staff.user.last_name = model.last_name
            staff.user.email = model.email
            staff.user.username = model.username
            staff.department = model.department
            staff.save()
            staff.user.save()
        except Staff.DoesNotExist as e:
            raise e

    def list_staff(self, model: ListStaffDto):
        staffs = list(Staff.objects.values('id',
                                           'user__first_name',
                                           'user__last_name',
                                           'user__email',
                                           'user__username',
                                           'role',
                                           'date_of_employment',
                                           'department'))

        results: List[ListStaffDto] = []
        for staff in staffs:
            item = ListStaffDto()
            item.first_name = staff['user__first_name']
            item.last_name = staff['user__last_name']
            item.email = staff['user__email']
            item.username = staff['user__username']
            item.department = staff['department']
            item.role = staff['role']
            item.date_of_employment = staff['date_of_employment']
            item.id = staff['id']
            results.append(item)
        return results

    def staff_details(self, user_id: int) -> StaffDetailsDto:
        try:
            staff = Staff.objects.get(user_id=user_id)
            result = StaffDetailsDto()
            result.first_name = staff.user.first_name
            result.last_name = staff.user.last_name
            result.email = staff.user.email
            result.username = staff.user.username
            result.role = staff.role
            result.department = staff.department
            result.date_of_employment = staff.date_of_employment
            result.id = staff.id
            return result
        except Staff.DoesNotExist as e:
            raise e

    def delete_staff(self, staff_id: int):
        try:
            Staff.objects.get(id=staff_id).delete()
        except Staff.DoesNotExist as e:
            raise e
