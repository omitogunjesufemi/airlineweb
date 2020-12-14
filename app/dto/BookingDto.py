from datetime import date


class RegisterBookingDto:
    flight_id: int
    passenger_id: int
    booking_reference: str
    flight_class: str
    seat_number: int
    price: int


class EditBookingDto:
    # flight_id: int
    flight_class: str
    price: int
    seat_number: int
    id: int


class ListBookingDto:
    flight_id: int
    passenger_id: int
    booking_reference: str
    flight_class: str
    price: int
    seat_number: int
    id: int


class GetBookingDto:
    flight_number: str
    take_off_location: str
    departure_date: str
    destination: str
    first_name: str
    last_name: str
    email: str
    phone: str
    booking_reference: str
    flight_class: str
    price: int
    passenger_id: int
    flight_id: int
    seat_number: int
    id: int


class BookingDetailsDto:
    flight_id: int
    passenger_id: int
    booking_reference: str
    flight_class: str
    price: int
    seat_number: int
    id: int

