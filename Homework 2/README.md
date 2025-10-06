# Movie Theater Booking Application

A full-stack Django web application for booking movie theater seats, featuring both a RESTful API and an interactive web interface built with Bootstrap.


## 🚀 Render Deployment

- **Deployed Application**: https://cs4300-9nct.onrender.com/
- **API Endpoints**: https://cs4300-9nct.onrender.com/api/
- **Admin Panel**: https://cs4300-9nct.onrender.com/admin/

## 📋 Prerequisites

- Python 3.12+
- pip (Python package manager)
- Git
- PostgreSQL (for production deployment)

## 🛠️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/WadePoltenovage/CS4300.git
cd "CS4300/Homework 2"
```

### 2. Create Virtual Environment

```bash
python3 -m venv myenv --system-site-packages
source myenv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Migrations

```bash
python3 manage.py migrate
```

### 5. Create Superuser

```bash
python3 manage.py createsuperuser
```

Follow the prompts to create an admin account.

### 6. Run Development Server

```bash
python3 manage.py runserver 0.0.0.0:3000
```

Visit `http://localhost:3000/` to view the application.

## 📁 Project Structure

```
Homework 2/
├── movie_theater_booking/      # Project settings
│   ├── settings.py            # Main settings
│   ├── production_settings.py # Production configuration
│   ├── urls.py                # Root URL configuration
│   └── wsgi.py                # WSGI configuration
├── bookings/                   # Main application
│   ├── models.py              # Data models (Movie, Seat, Booking)
│   ├── views.py               # ViewSets and template views
│   ├── serializers.py         # DRF serializers
│   ├── urls.py                # App URL routing
│   ├── admin.py               # Admin panel configuration
│   ├── tests.py               # Unit and integration tests
│   └── templates/             # HTML templates
│       └── bookings/
│           ├── base.html      # Base template with Bootstrap
│           ├── movie_list.html
│           ├── seat_booking.html
│           └── booking_history.html
├── manage.py                  # Django management script
├── requirements.txt           # Python dependencies
├── build.sh                   # Render build script
├── render.yaml                # Render deployment config
└── README.md                  # This file
```

## 🌐 API Endpoints

### Movies
- `GET /api/movies/` - List all movies
- `POST /api/movies/` - Create a new movie
- `GET /api/movies/{id}/` - Get movie details
- `PUT /api/movies/{id}/` - Update movie
- `DELETE /api/movies/{id}/` - Delete movie
- `GET /api/movies/{id}/seats/` - Get seats for a movie

### Seats
- `GET /api/seats/` - List all seats
- `POST /api/seats/` - Create a new seat
- `GET /api/seats/{id}/` - Get seat details
- `GET /api/seats/available/` - Get available seats
- `POST /api/seats/{id}/book/` - Book a seat

### Bookings
- `GET /api/bookings/` - List all bookings
- `POST /api/bookings/` - Create a booking
- `GET /api/bookings/{id}/` - Get booking details
- `GET /api/bookings/my_bookings/` - Get current user's bookings

## 🎨 Web Interface

- **Home (`/`)**: Browse all available movies
- **Seat Booking (`/book/{movie_id}/`)**: Select and book seats for a specific movie
- **Booking History (`/history/`)**: View all bookings
- **Admin Panel (`/admin/`)**: Manage movies, seats, and bookings

## 🧪 Running Tests

Run all tests:
```bash
python manage.py test
```

Run specific test class:
```bash
python manage.py test bookings.tests.MovieModelTest
```

Run with verbose output:
```bash
python manage.py test --verbosity=2
```

### Test Coverage

The test suite includes:
- **Unit Tests**: Model creation, validation, and constraints
- **Integration Tests**: API endpoints (CRUD operations)
- **Template Tests**: View rendering and form submissions

Total: 26 tests covering models, API, and templates.


## 🤖 AI Usage Disclosure

This project was developed with assistance from Claude (Anthropic) AI assistant. AI was used for:

- **Code Generation**: Utilized for setting up the django backend as I have never done that before and needed some guidance
- **Troubleshooting**: I ran into some problems where I was either missing important syntax, was having trouble getting setting up the render initially
- **Documentation**: Cleaned up and made my README pretty as well as commenting some code I was having some trouble with.
- **Testing**: Used to create some test cases looking for fail points I may not have thought of.

All AI-generated code was reviewed, tested, and modified as needed to meet project requirements.
