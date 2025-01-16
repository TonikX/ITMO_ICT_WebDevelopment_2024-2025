### Список рейсов
```
class FlightsList(ListView):
    model = Flight
    template_name = 'flights/list.html'
    context_object_name = 'flights'
    paginate_by = 10
```

### Информация о рейсе
```
@login_required(login_url='/accounts/login/')
def flight_detail(request, flight_id):
    flight = get_object_or_404(Flight, id=flight_id)
    tickets = Ticket.objects.filter(flight=flight)
    reviews = FlightReview.objects.filter(flight=flight)
    has_reviewed = FlightReview.objects.filter(flight=flight, author=request.user).exists()

    return render(request, 'flights/detail.html', {
        'flight': flight,
        'tickets': tickets,
        'reviews': reviews,
        'has_reviewed': has_reviewed,
        'form': ReviewForm()
    })
```

### Добавить отзыв о рейсе
```
@login_required(login_url='/accounts/login/')
def add_review(request, flight_id):
    flight = get_object_or_404(Flight, id=flight_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.flight = flight
            review.author = request.user
            review.save()
            return redirect('flight_details', flight_id=flight.id)
    else:
        form = ReviewForm()

    return render(request, 'reviews/add.html', {'flight': flight, 'form': form})
```

### Изменить билет
```
def edit_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if request.method == "POST":
        form = TicketForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            messages.success(request, "Ticket updated successfully.")
            return redirect('flight_details', flight_id=ticket.flight.id)
    else:
        form = TicketForm(instance=ticket)

    return render(request, 'tickets/edit.html', {'form': form, 'ticket': ticket})
```

### Удалить бронь билета
```
def delete_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.method == "POST":
        ticket.delete()
        messages.success(request, "Ticket deleted successfully.")
        return redirect('flight_details', flight_id=ticket.flight.id)

    return render(request, 'tickets/delete.html', {'ticket': ticket})
```

### Забронировать билет
```
@login_required(login_url='/accounts/login/')
def reserve_ticket(request, flight_id):
    flight = get_object_or_404(Flight, id=flight_id)
    if request.method == 'POST':
        form = TicketReservationForm(request.POST, flight=flight)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.flight = flight
            ticket.passenger = request.user
            ticket.save()
            return redirect('flight_details', flight_id=flight.id)
    else:
        form = TicketReservationForm(flight=flight)
    return render(request, 'tickets/reserve.html', {'flight': flight, 'form': form})
```