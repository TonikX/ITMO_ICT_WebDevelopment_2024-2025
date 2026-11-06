# Routes and functionality

## Public pages

| URL | Method | Description |
| --- | --- | --- |
| `/` | GET | Catalogue, search, country filter, pagination |
| `/tour/<id>/` | GET | Tour description, dates, price, payment conditions, reviews |
| `/register/` | GET, POST | Registration |
| `/login/` | GET, POST | Login |
| `/logout/` | POST | Logout |
| `/sold-tours/` | GET | Confirmed tours by country, sold places and estimated value |

## Authenticated customer pages

| URL | Method | Description |
| --- | --- | --- |
| `/tour/<id>/book/` | GET, POST | Create a pending booking |
| `/bookings/` | GET | See only one's own reservations |
| `/bookings/<id>/edit/` | GET, POST | Edit a pending reservation |
| `/bookings/<id>/delete/` | GET, POST | Confirm deletion of a pending reservation |
| `/tour/<id>/review/` | GET, POST | Review a completed tour with a confirmed booking |

## Staff-only pages

| URL | Method | Description |
| --- | --- | --- |
| `/staff/` | GET | Pending bookings and sales summary |
| `/staff/bookings/<id>/confirm/` | POST | Confirm a booking |
| `/staff/bookings/<id>/cancel/` | POST | Cancel a booking |
| `/admin/` | GET, POST | Django Admin for authorized staff |

Staff links appear only for staff users. Server-side decorators also block direct access to staff endpoints by ordinary customers. All state-changing form submissions use CSRF protection.

## Catalogue and filtering

The main page shows up to six tours. Users can search by tour title, description or country and limit results to a country. Page links preserve the selected filters. Only active tours appear in the catalogue, while an inactive sold tour remains viewable through its historical sale record.

## Booking workflow

1. The user selects an upcoming tour and the number of travellers.
2. Django creates a reservation with `pending` status.
3. The customer can change or delete their own pending booking.
4. An administrator confirms it through Django Admin or the staff dashboard.
5. The transaction decreases the number of free seats and sets `confirmed`.
6. If the administrator cancels the booking, seats are restored and status becomes `cancelled`.

The confirmation logic uses two locked rows to keep status and remaining seats consistent:

```python
tour = Tour.objects.select_for_update().get(pk=booking.tour_id)
if booking.persons > tour.available_seats:
    return redirect("staff_dashboard")
tour.available_seats -= booking.persons
tour.save(update_fields=["available_seats"])
booking.status = Booking.Status.CONFIRMED
booking.save(update_fields=["status"])
```

## Reviews

The application checks for a confirmed booking, verifies that the trip has ended and prevents a second review by the same author for the same tour. A score between 1 and 10 is required. The `Review` model stores a snapshot of the tour dates to preserve the historical period.

## Sales by country

The public sales table shows the destination country, tour name, number of confirmed reservations, number of places sold and estimated value. The separate staff dashboard summarizes these figures by country.

## Template engine and design

The client-facing pages are rendered by the Jinja2 backend. Django Templates is retained for Django Admin's built-in interface. Bootstrap 5 and project CSS style the catalogue, navigation, forms and tables.

## Verification

Run the automated Django tests with `python manage.py test tours`. They cover admin booking actions, tour validation, filtering, registration, user ownership, booking editing and deletion, staff confirmation, sales, completed-trip reviews, historical dates and pagination.
