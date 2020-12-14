class CreateStaffDto:
    first_name: str
    last_name: str
    password: str
    confirm_password: str
    email: str
    username: str


class EditStaffDto:
    first_name: str
    last_name: str
    email: str
    username: str


class ListStaffDto:
    first_name: str
    last_name: str
    email: str
    username: str


class StaffDetailsDto:
    first_name: str
    last_name: str
    email: str
    username: str