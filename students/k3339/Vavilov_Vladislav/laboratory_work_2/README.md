# Laboratory Work 2 — TravelWay

**Student:** Vavilov Vladislav  
**University:** ITMO University  
**Discipline:** Web Programming  
**Variant:** 4 — Travel agency tour catalogue

TravelWay is a Django application with Jinja2 templates and a PostgreSQL database. It supports user registration, tour search, country filters, pagination, tour bookings, completed-trip reviews and sales reports.

## Implemented requirements

- Tour information: agency, country, description, dates, price, payment terms and remaining places.
- Registration, authentication and personal booking management.
- Booking creation, editing and deletion while the booking is pending.
- Reviews with rating 1–10, author, text and a historical snapshot of the tour dates.
- Booking confirmation and cancellation from Django Admin and the staff-facing website.
- Sold tours by country, including bookings, places sold and estimated revenue.
- Bootstrap styling, pagination, search, filtering and server-side role checks.
- Documentation with MkDocs and automated tests.

## Setup on Windows (PowerShell)

Install Python 3.12+ and PostgreSQL. Create a new, empty PostgreSQL database named `travel_agency_lab2` and grant your PostgreSQL user access to it. The configuration assumes the database user is `postgres`, port `5432` and host `localhost`. Use a separate database from your earlier draft so existing records remain untouched.

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Open `.env` and set a unique `DJANGO_SECRET_KEY` and the local PostgreSQL `DB_PASSWORD`. Keep JSON quotes around values. The `DB_NAME` setting points to the separate demonstration database. Never commit or share `.env`.

```powershell
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py loaddata fixtures/demo_tours.json
.\.venv\Scripts\python.exe manage.py seed_demo_sales
.\.venv\Scripts\python.exe manage.py createsuperuser
.\.venv\Scripts\python.exe manage.py runserver
```

Open <http://127.0.0.1:8000/>. The fixture and sales command are intended for a new, empty demonstration database, not the populated database from your previous draft. The sales command can be run again without duplicating demo bookings. It creates a demonstration account with an unusable password, five confirmed reservations across four countries and a review of a completed tour.

## Setup on Linux / macOS

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
cp .env.example .env
```

After configuring `.env` and PostgreSQL, use `.venv/bin/python` in place of `.\.venv\Scripts\python.exe` for the remaining commands.

## Checks

```powershell
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py makemigrations --check --dry-run
.\.venv\Scripts\python.exe manage.py test tours
```

## Documentation

```powershell
.\.venv\Scripts\python.exe -m mkdocs serve -a 127.0.0.1:8001
```

Open <http://127.0.0.1:8001/>. Source pages are in `docs/`. The generated `site/` directory is ignored. Publish the MkDocs report on GitHub Pages through the current course repository.

## Submission

According to the laboratory assignment, the project must be placed in the course repository at:

```text
students/группа/laboratory_works/фамилия_имя/laboratory_work_2
```

Use the actual group and student directory names required by the repository. Submit the application source, migrations, fixtures, tests and MkDocs report sources together. The report must describe variant 4 and the implemented interfaces. Do not submit the local database, passwords, virtual environment or generated documentation site.

## Important routes

| URL | Purpose |
| --- | --- |
| `/` | Tour catalogue, search, filters and pagination |
| `/register/`, `/login/` | Registration and authentication |
| `/tour/<id>/` | Tour details and reviews |
| `/bookings/` | Personal reservations |
| `/sold-tours/` | Sold tours by destination country |
| `/staff/` | Staff booking management and country-level sales |
| `/admin/` | Django Admin |

See the MkDocs **Routes and functionality** section for all endpoints and their access rules.

## Repository hygiene

Commit only source code, migrations, documentation, fixtures, tests and dependency manifests. Do not include `.env`, `.venv/`, `db.sqlite3`, `__pycache__/` or the generated `site/` directory.
