from datetime import date


class RegisterAircraftDto:
    aircraft_name: str
    aircraft_type: str
    aircraft_number: str
    capacity: int
    date_created: date


class EditAircraftDto:
    aircraft_name: str
    aircraft_type: str
    capacity: int
    date_updated: date
    aircraft_id: int


class ListAircraftDto:
    aircraft_name: str
    aircraft_type: str
    aircraft_number: str
    capacity: int
    date_updated: date
    date_created: date
    id: int


class AircraftDetailsDto:
    aircraft_name: str
    aircraft_type: str
    aircraft_number: str
    capacity: int
    date_updated: date
    date_created: date
    id: int

