# Database

The application is configured for PostgreSQL and uses Django ORM for models, queries and transactions.

| Setting | Local value |
| --- | --- |
| Database engine | PostgreSQL |
| Database name | `travel_agency_lab2` |
| Host | `localhost` |
| Port | `5432` |
| User | `postgres` |
| Password | Taken from the local, uncommitted `.env` file |

## Preparation

After creating this separate, empty database, copy `.env.example` to `.env`, provide a secret key and database password, and run:

```powershell
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py loaddata fixtures/demo_tours.json
```

The fixture includes four countries, one travel agency and nine tours. It includes a completed 2026 tour for demonstrating reviews and enough upcoming trips to show pagination.

To populate demonstration sales on an otherwise empty database:

```powershell
.\.venv\Scripts\python.exe manage.py seed_demo_sales
```

This command creates five confirmed bookings across four countries, adjusts available places and adds a completed-trip review. It is repeatable without duplicating the same demo records. It creates no usable login password.

## Querying and updating data

The catalogue uses `select_related()` to retrieve tours with their agencies and countries. Search filters use `icontains`, and the catalogue is paginated six tours at a time.

Confirmation and cancellation use `transaction.atomic()` and `select_for_update()`. The first locks affected booking and tour rows, then updates status and remaining places in one database transaction.

The public sold-tours report groups confirmed bookings by tour and country. The staff dashboard aggregates confirmed bookings, travellers and estimated revenue by country.

Revenue is based on the current tour price, not on a separate payment transaction; it is therefore displayed as an estimate rather than collected revenue.
