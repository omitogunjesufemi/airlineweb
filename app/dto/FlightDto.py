from datetime import date, time
from app.models import Aircraft


class RegisterFlightDto:
    aircraft_id: int
    flight_number: str
    take_off_location: str
    price: float
    arrival_time: time
    destination: str
    departure_date: date
    date_created: date


class EditFlightDto:
    aircraft_id: int
    flight_number: str
    take_off_location: str
    price: float
    arrival_time: time
    destination: str
    departure_date: date
    date_updated: date
    id: int


class ListFlightDto:
    aircraft_id: int
    flight_number: str
    take_off_location: str
    price: float
    arrival_time: time
    destination: str
    departure_date: date
    date_created: date
    date_updated: date
    id: int


class FlightDetailDto:
    aircraft_id: int
    aircraft_name: str
    flight_number: str
    take_off_location: str
    price: float
    arrival_time: time
    destination: str
    departure_date: date
    date_created: date
    date_updated: date
    id: int

