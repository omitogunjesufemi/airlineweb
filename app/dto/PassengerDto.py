from datetime import date


class RegisterPassengerDto:
    first_name: str
    last_name: str
    email: str
    phone: str
    address: str
    registration_number: str
    # date_created: date
    id: int


class EditPassengerDto:
    first_name: str
    last_name: str
    email: str
    phone: str
    address: str
    registration_number: str
    # date_updated: date
    id: int


class ListPassengerDto:
    first_name: str
    last_name: str
    email: str
    phone: str
    address: str
    registration_number: str
    # date_created: date
    # date_updated: date
    id: int


class PassengerDetailsDto:
    first_name: str
    last_name: str
    email: str
    phone: str
    address: str
    registration_number: str
    # date_created: date
    # date_updated: date
    id: int
