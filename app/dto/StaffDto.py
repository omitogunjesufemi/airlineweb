from datetime import date


class RegisterStaffDto:
    first_name: str
    last_name: str
    password: str
    confirm_password: str
    email: str
    username: str
    role: str
    department: str
    date_of_employment: date


class EditStaffDto:
    first_name: str
    last_name: str
    email: str
    username: str
    role: str
    department: str
    date_of_employment: date
    id: int


class ListStaffDto:
    first_name: str
    last_name: str
    email: str
    username: str
    role: str
    department: str
    date_of_employment: date


class StaffDetailsDto:
    first_name: str
    last_name: str
    email: str
    username: str
    role: str
    department: str
    date_of_employment: date