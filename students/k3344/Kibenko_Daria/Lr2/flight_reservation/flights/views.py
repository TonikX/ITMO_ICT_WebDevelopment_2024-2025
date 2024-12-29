from django.shortcuts import render

flights_data = [
    {"flight_number": "AB123", "airline": "Airline A", "destination": "City X"},
    {"flight_number": "CD456", "airline": "Airline B", "destination": "City Y"},
    {"flight_number": "EF789", "airline": "Airline C", "destination": "City Z"},
]

reservations_data = []


def flight_list(request):
    return render(request, 'flights/flight_list.html', {'flights': flights_data})


def my_reservations(request):
    return render(request, 'flights/my_reservations.html', {'reservations': reservations_data})


def reserve_flight(request, flight_number):
    if request.method == "POST":
        seat_number = request.POST.get('seat_number')
        reservations_data.append({"flight_number": flight_number, "seat_number": seat_number})
    return render(request, 'flights/my_reservations.html', {'reservations': reservations_data})

