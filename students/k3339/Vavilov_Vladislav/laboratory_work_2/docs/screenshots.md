# Screenshots

The screenshots were captured during functional checks with PostgreSQL. They show different stages of the demonstration: booking statuses and available seats can change between images.

## Registration and authentication

The registration form creates a customer account. After successful registration, the customer is signed in and can access personal bookings.

![User registration form](screenshots/09_registration.png)

![Successful registration and automatic login](screenshots/15_registration_success.png)

## Tour catalogue and pagination

The catalogue shows search by title or country, a country filter, prices, dates and available places. Nine sample tours appear across two pages: six on the first page and three on the second.

![Tour catalogue](screenshots/01_tours.png)

![First catalogue page](screenshots/13_pagination_first.png)

![Second catalogue page](screenshots/14_pagination_second.png)

## Tour details and published review

The tour page displays the organizing agency, trip dates, payment terms, price and available places. The completed Venice tour cannot be booked again. Its historical review records a rating of 9/10, the author, travel dates and publication time.

![Completed tour details and published review](screenshots/02_tour_detail.png)

## Customer booking management

A registered customer creates a reservation with **Pending** status. The customer can edit or delete their own pending booking. In the demonstrated edit, the number of travellers changes from two to three and the total changes from 170,000 to 255,000 rubles.

![Pending customer booking](screenshots/03_pending_booking.png)

![Editing the number of travellers](screenshots/16_edit_booking.png)

![Updated booking and recalculated total](screenshots/17_updated_booking.png)

## Confirmation in Django Admin

Django Admin manages agencies, tours, countries, bookings and reviews. The booking record for `felicia` contains three travellers and initially has **Pending** status.

![Django Admin overview](screenshots/08_django_admin.png)

![Pending reservation in Django Admin](screenshots/18_admin_pending_booking.png)

The administrator selects **Confirm selected bookings** and confirms the booking. The later screenshot shows the user's reservation as **Confirmed**. The demonstration records were also cancelled during subsequent manual testing, so their statuses differ between the screenshots.

![Selecting the booking confirmation action](screenshots/05_sales.png)

![Confirmed booking in Django Admin](screenshots/06_confirmed_booking.png)

## Staff interface on the website

In addition to Django Admin, staff have a dedicated customer-facing administration page with controls to confirm or cancel pending bookings and a sales summary by country. Ordinary customers cannot access this page.

![Staff booking management and sales by country](screenshots/04_pending_staff.png)

## Public sold-tours report

The public table displays only confirmed bookings, grouped by tour and destination country, including the number of reservations, places sold and estimated value.

![Sold tours by destination country](screenshots/11_sold_tours.png)

## Automated verification

All 22 Django tests passed against PostgreSQL, with no Django system-check issues.

![Successful Django tests on PostgreSQL](screenshots/12_tests.png)

## MkDocs report

The report is built with MkDocs Material and includes the variant description, data models, database details, routes, functionality and screenshots.

![MkDocs documentation site](screenshots/10_mkdocs.png)
