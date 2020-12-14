from typing import Callable

from dependency_injector import providers, containers
from app.repositories.AircraftRepository import AircraftRepository, DjangoORMAircraftRepository
from app.services.AirlineManagementService import AirlineManagementService, DefaultAirlineManagementService
from app.repositories.FlightRepository import FlightRepository, DjangoORMFlightRepository
from app.services.FlightManagementService import FlightManagementService, DefaultFlightManagementService
from app.repositories.PassengerRepository import PassengerRepository, DjangoORMPassengerRepository
from app.services.PassengerManagementServices import PassengerManagementService, DefaultPassengerManagementService
from app.repositories.BookingRepository import BookingRepository, DjangoORMBookingRepository
from app.services.BookingManagementService import BookingManagementService, DefaultBookingManagementService


class Container(containers.DeclarativeContainer):
    # AIRCRAFT SERVICE PROVIDER
    aircraft_repository: Callable[[], AircraftRepository] = providers.Factory(
        DjangoORMAircraftRepository
    )

    aircraft_management_service: Callable[[], AirlineManagementService] = providers.Factory(
        DefaultAirlineManagementService,
        repository=aircraft_repository
    )

    # FLIGHT SERVICE PROVIDER
    flight_repository: Callable[[], FlightRepository] = providers.Factory(
        DjangoORMFlightRepository
    )
    flight_management_service: Callable[[], FlightManagementService] = providers.Factory(
        DefaultFlightManagementService,
        repository=flight_repository
    )

    # PASSENGER SERVICE PROVIDER
    passenger_repository: Callable[[], PassengerRepository] = providers.Factory(
        DjangoORMPassengerRepository
    )
    passenger_management_service: Callable[[], PassengerManagementService] = providers.Factory(
        DefaultPassengerManagementService,
        repository=passenger_repository
    )

    # BOOKING SERVICE PROVIDER
    booking_repository: Callable[[], BookingRepository] = providers.Factory(
        DjangoORMBookingRepository
    )
    booking_management_service: Callable[[], BookingManagementService] = providers.Factory(
        DefaultBookingManagementService,
        repository=booking_repository
    )


airline_service_provider = Container()
