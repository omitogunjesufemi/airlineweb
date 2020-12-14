from typing import List
from django.shortcuts import redirect, render
from app.dto.FlightDto import ListFlightDto
from app.models import Flight
from app.service_provider import airline_service_provider


def index(request):
    context = {
        'flights': 'Nothing to display'
    }
    if request.method == 'POST':
        __get_search_parameters(request, context)
        return render(request, 'flight/index_search.html', context)
    return render(request, 'index.html', context)


def __get_search_parameters(request, context):
    take_off_location = request.POST['take_off_location']
    destination = request.POST['destination']
    departure_date = request.POST['departure_date']
    try:
        flights = airline_service_provider.flight_management_service().list_flight()
        flights_list: List[ListFlightDto] = []

        for flight in flights:
            if take_off_location == flight.take_off_location:
                if destination == flight.destination:
                    if departure_date == flight.departure_date:
                        flights_list.append(flight)

                    flights_list.append(flight)

                pass

            pass

        context['flights'] = flights_list

    except Flight.DoesNotExist as e:
        print('No flight to display')
        raise e