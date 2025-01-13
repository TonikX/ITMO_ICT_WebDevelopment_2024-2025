# Conference Site

Conference Site is a web application built with Django and PostgreSQL that allows users to register for scientific conferences, leave reviews, and view participant lists. Administrators can manage conference details and presentation results.

## Features

- User registration and authentication
- Browse and register for conferences
- Edit and delete conference registrations
- Leave reviews for attended conferences
- Admin panel for managing conferences and results
- Pagination and search functionality for conferences
- Responsive design with Bootstrap

## Installation

### Prerequisites

- Python 3.12
- PostgreSQL
- poetry

### Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/conference-site.git
   cd conference-site
   ```

2. **Create and activate a virtual environment, install all needed libs:**

   ```bash
   poetry shell
   ```

3. **Configure the database:**

   - Create a PostgreSQL database and user.
   - Update the `DATABASES` settings in `conference_site/settings.py` with your database credentials.

4. **Apply migrations:**

   ```bash
   python manage.py migrate
   ```

5. **Create a superuser:**

   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server:**

   ```bash
   python manage.py runserver
   ```

7. **Access the application:**

   - Open your web browser and go to `http://127.0.0.1:8000/`.

## Usage

- **Register** as a new user or **log in** if you already have an account.
- Browse the list of available conferences.
- Register for conferences you are interested in.
- Leave reviews for conferences you have attended.
- Administrators can log in to the admin panel at `http://127.0.0.1:8000/admin/` to manage conferences and results.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to the Django community for their excellent documentation and resources.
- Bootstrap for providing a responsive design framework.