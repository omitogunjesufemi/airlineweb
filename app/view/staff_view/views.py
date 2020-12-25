from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from app.decorators import allowed_users
from app.dto.StaffDto import EditStaffDto
from app.models import Staff
from app.service_provider import airline_service_provider


@login_required(login_url='login')
@allowed_users(['staffs'])
def list_staff(request):
    staffs = airline_service_provider.staff_management_service().list_staff()
    context = {
        'staffs': staffs,
    }
    return render(request, '', context)


@login_required(login_url='login')
@allowed_users(['staffs'])
def staff_home(request):
    user_id = request.user.id
    staff = airline_service_provider.staff_management_service().staff_details(user_id=user_id)
    context = {
        'welcome': "Welcome to the Staff HomePage!",
        'staff': staff,
    }
    return render(request, 'staff/staff_home.html', context)


@login_required(login_url='login')
@allowed_users(['staffs'])
def edit_staff(request):
    user_id = request.user.id
    staff = airline_service_provider.staff_management_service().staff_details(user_id=user_id)
    context = {
        'staff': staff,

    }
    new_staff = __edit_if_post_method(request, context)
    if new_staff is not None:
        context['staff'] = new_staff
        return redirect('staff_home')
    return render(request, 'staff/staff_edit.html', context)


def __edit_if_post_method(request, context):
    if request.method == 'POST':
        try:
            user_id = request.user.id
            staff = Staff.objects.get(user_id=user_id)
            staff_id = staff.id
            edited_staff = __set_staff_edited_details(request, staff_id)
            airline_service_provider.staff_management_service().edit_staff(staff_id, edited_staff)
            context['saved'] = 'success'
            return __get_staff_details_or_raise_error(user_id=user_id)
        except Staff.DoesNotExist as e:
            raise e


def __get_staff_edited_details(request, edit_staff_dto):
    edit_staff_dto.first_name = request.POST['first_name']
    edit_staff_dto.last_name = request.POST['last_name']
    edit_staff_dto.username = request.POST['username']
    edit_staff_dto.email = request.POST['email']
    edit_staff_dto.department = request.POST['department']
    edit_staff_dto.role = request.POST['role']
    edit_staff_dto.date_of_employment = request.POST['date_of_employment']


def __set_staff_edited_details(request, staff_id):
    edit_staff_dto = EditStaffDto()
    edit_staff_dto.id = staff_id
    edit_staff_dto.first_name = request.POST['first_name']
    __get_staff_edited_details(request, edit_staff_dto)
    return edit_staff_dto


def __get_staff_details_or_raise_error(user_id):
    try:
        return airline_service_provider.staff_management_service().staff_details(user_id=user_id)
    except Staff.DoesNotExist as e:
        raise e
