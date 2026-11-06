# Data models

TravelWay uses Django's built-in user model plus five application models. All database relationships are implemented with Django ORM foreign keys.

| Model | Main fields | Relationships |
| --- | --- | --- |
| `Country` | Unique country name | One country has many tours |
| `Agency` | Name, address, phone, email | One agency organizes many tours |
| `Tour` | Title, description, start/end dates, price, payment terms, available seats, active flag | Foreign keys to agency and country |
| `Booking` | User, tour, persons, status, creation time | Foreign keys to user and tour |
| `Review` | User, tour, saved tour start/end dates, rating, text, publication time | Foreign keys to user and tour |

## Tour

The period is stored as `start_date` and `end_date`. The model rejects an end date before the start date and a zero or negative price. Payment conditions are stored in `payment_terms`. `available_seats` counts places not yet confirmed as sold.

## Booking

The booking connects a customer with a tour and stores the number of travellers. Its possible statuses are `pending`, `confirmed` and `cancelled`.

- Pending: editable and removable by the customer while the tour is still available.
- Confirmed: the administrator has approved the reservation and the number of available places decreases.
- Cancelled: a previously confirmed reservation returns its places to the tour.

The interface blocks changes to processed reservations. Confirmation uses a database transaction and row locks so that multiple administrators cannot oversell the same seats.

## Review

Reviews include a score between 1 and 10, the author, the text and the period of the tour at the time of the review. The dates are copied into the review when it is created, so editing the tour later does not change historical reviews.

A customer can publish one review per tour after its end date and only if they have a confirmed booking. A uniqueness constraint prevents duplicate reviews for the same user and tour.

## Database relationships

`Country → Tour ← Agency`  
`User → Booking ← Tour`  
`User → Review ← Tour`

The initial tables and subsequent field changes are recorded in the Django migration files in `tours/migrations/`.
