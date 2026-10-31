# Laboratory Work 2 — TravelWay

## Variant 4 — Travel agency tour catalogue

**Student:** Vavilov Vladislav  
**Discipline:** Web Programming  
**University:** ITMO University

## Purpose

Build a tourism web application with Django, Jinja2 and PostgreSQL. Customers should be able to find and reserve tours, manage pending bookings and review completed trips. Administrators must confirm reservations, and the website must display sold tours by destination country.

## Technology stack

| Component | Technology |
| --- | --- |
| Server-side application | Python 3, Django 5.2 |
| Customer-facing templates | Jinja2 3.1 |
| Database | PostgreSQL, Django ORM |
| Administrator interface | Django Admin |
| UI styling | Bootstrap 5, custom CSS |
| Documentation | MkDocs Material |

## Implemented functionality

- Registration, login and logout.
- Tour cards with country, dates, price and available places.
- Search, country filtering and pagination (six tours per page).
- Tour details with the organizing agency and payment conditions.
- Booking creation, editing and deletion by its owner while pending.
- Admin and staff confirmation or cancellation of bookings; correct available-seat updates.
- Reviews after a trip is completed, with author, rating (1–10), text and saved trip dates.
- Public table of sold tours by country and a staff-level summary of sales.

## Compliance with the assignment

| Requirement for variant 4 | Implementation |
| --- | --- |
| Tour title, agency, description, dates and payment terms | Tour model, catalogue and tour detail page |
| Registration of new users | Registration form and automatic login |
| View, reserve, edit and delete own bookings | Tour detail, booking form and personal bookings page |
| Reviews with trip dates, author, text and rating 1–10 | Review model and completed-tour review page |
| Confirmation through Django Admin | Booking administration action, seat availability update |
| Public list of sold tours by country | Sold tours page with confirmed bookings |
| CSS design | Bootstrap and custom project styles |
| Pagination, filtering and search | Six tours per page, country dropdown, text search |
| Separate customer and staff capabilities on the website | Staff dashboard and server-side access checks |

## Demonstration scenario

1. Load nine example tours in four destination countries.
2. Create a customer account, open a future tour and make a booking.
3. Sign in as staff, confirm the reservation and check the updated seat count.
4. Open **Sold tours** to see a confirmed sale.
5. View a completed tour to see a review with a rating and travel dates.

The optional `seed_demo_sales` command prepares five confirmed demonstration bookings across all four countries. The **Screenshots** section illustrates the key user interfaces.

## Structure of the report

- **Data models:** entity fields, relationships and validation rules.
- **Database:** PostgreSQL configuration, migrations and demonstration data.
- **Routes and functionality:** client interfaces, permissions, booking and review workflows.
- **Screenshots:** visual evidence of the application.
