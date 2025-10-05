from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from datetime import date
from .models import Movie, Seat, Booking


class MovieModelTest(TestCase):
    """Unit tests for Movie model"""

    def setUp(self):
        """Set up test data"""
        self.movie = Movie.objects.create(
            title="Test Movie",
            description="A test movie description",
            release_date=date(2024, 1, 1),
            duration=120
        )

    def test_movie_creation(self):
        """Test that a movie can be created"""
        self.assertEqual(self.movie.title, "Test Movie")
        self.assertEqual(self.movie.duration, 120)
        self.assertIsInstance(self.movie, Movie)

    def test_movie_str(self):
        """Test the string representation of movie"""
        self.assertEqual(str(self.movie), "Test Movie")

    def test_movie_ordering(self):
        """Test that movies are ordered by release date"""
        movie2 = Movie.objects.create(
            title="Earlier Movie",
            description="Released earlier",
            release_date=date(2023, 1, 1),
            duration=90
        )
        movies = Movie.objects.all()
        self.assertEqual(movies[0], movie2)
        self.assertEqual(movies[1], self.movie)


class SeatModelTest(TestCase):
    """Unit tests for Seat model"""

    def setUp(self):
        """Set up test data"""
        self.movie = Movie.objects.create(
            title="Test Movie",
            description="Test",
            release_date=date(2024, 1, 1),
            duration=120
        )
        self.seat = Seat.objects.create(
            seat_number="A1",
            status="available",
            movie=self.movie
        )

    def test_seat_creation(self):
        """Test that a seat can be created"""
        self.assertEqual(self.seat.seat_number, "A1")
        self.assertEqual(self.seat.status, "available")
        self.assertEqual(self.seat.movie, self.movie)

    def test_seat_str(self):
        """Test the string representation of seat"""
        self.assertEqual(str(self.seat), "Seat A1 - available")

    def test_seat_status_choices(self):
        """Test seat status choices"""
        self.seat.status = "booked"
        self.seat.save()
        self.assertEqual(self.seat.status, "booked")

    def test_seat_unique_per_movie(self):
        """Test that seat numbers are unique per movie"""
        # Same seat number for different movie should work
        movie2 = Movie.objects.create(
            title="Another Movie",
            description="Test",
            release_date=date(2024, 2, 1),
            duration=100
        )
        seat2 = Seat.objects.create(
            seat_number="A1",
            status="available",
            movie=movie2
        )
        self.assertEqual(seat2.seat_number, "A1")
        self.assertNotEqual(seat2.movie, self.seat.movie)


class BookingModelTest(TestCase):
    """Unit tests for Booking model"""

    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )
        self.movie = Movie.objects.create(
            title="Test Movie",
            description="Test",
            release_date=date(2024, 1, 1),
            duration=120
        )
        self.seat = Seat.objects.create(
            seat_number="A1",
            status="available",
            movie=self.movie
        )
        self.booking = Booking.objects.create(
            movie=self.movie,
            seat=self.seat,
            user=self.user
        )

    def test_booking_creation(self):
        """Test that a booking can be created"""
        self.assertEqual(self.booking.movie, self.movie)
        self.assertEqual(self.booking.seat, self.seat)
        self.assertEqual(self.booking.user, self.user)
        self.assertIsNotNone(self.booking.booking_date)

    def test_booking_str(self):
        """Test the string representation of booking"""
        expected = f"{self.user.username} - {self.movie.title} - Seat {self.seat.seat_number}"
        self.assertEqual(str(self.booking), expected)

    def test_booking_unique_constraint(self):
        """Test that same seat cannot be booked twice for same movie"""
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            Booking.objects.create(
                movie=self.movie,
                seat=self.seat,
                user=self.user
            )


class MovieAPITest(APITestCase):
    """Integration tests for Movie API"""

    def setUp(self):
        """Set up test data"""
        self.movie = Movie.objects.create(
            title="API Test Movie",
            description="Testing the API",
            release_date=date(2024, 1, 1),
            duration=120
        )
        self.url = reverse('movie-list')

    def test_get_movie_list(self):
        """Test retrieving movie list"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_movie_detail(self):
        """Test retrieving a single movie"""
        url = reverse('movie-detail', args=[self.movie.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "API Test Movie")

    def test_create_movie(self):
        """Test creating a new movie"""
        data = {
            'title': 'New Movie',
            'description': 'A new test movie',
            'release_date': '2024-06-01',
            'duration': 150
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Movie.objects.count(), 2)

    def test_update_movie(self):
        """Test updating a movie"""
        url = reverse('movie-detail', args=[self.movie.id])
        data = {
            'title': 'Updated Movie',
            'description': 'Updated description',
            'release_date': '2024-01-01',
            'duration': 130
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.movie.refresh_from_db()
        self.assertEqual(self.movie.title, 'Updated Movie')

    def test_delete_movie(self):
        """Test deleting a movie"""
        url = reverse('movie-detail', args=[self.movie.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Movie.objects.count(), 0)


class SeatAPITest(APITestCase):
    """Integration tests for Seat API"""

    def setUp(self):
        """Set up test data"""
        self.movie = Movie.objects.create(
            title="Test Movie",
            description="Test",
            release_date=date(2024, 1, 1),
            duration=120
        )
        self.seat = Seat.objects.create(
            seat_number="B1",
            status="available",
            movie=self.movie
        )
        self.url = reverse('seat-list')

    def test_get_seat_list(self):
        """Test retrieving seat list"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_available_seats(self):
        """Test retrieving only available seats"""
        Seat.objects.create(
            seat_number="B2",
            status="booked",
            movie=self.movie
        )
        url = reverse('seat-available')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['status'], 'available')

    def test_book_seat(self):
        """Test booking a seat"""
        url = reverse('seat-book', args=[self.seat.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.seat.refresh_from_db()
        self.assertEqual(self.seat.status, 'booked')

    def test_book_already_booked_seat(self):
        """Test booking an already booked seat"""
        self.seat.status = 'booked'
        self.seat.save()
        url = reverse('seat-book', args=[self.seat.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class BookingAPITest(APITestCase):
    """Integration tests for Booking API"""

    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username="apiuser",
            password="testpass123"
        )
        self.movie = Movie.objects.create(
            title="Test Movie",
            description="Test",
            release_date=date(2024, 1, 1),
            duration=120
        )
        self.seat = Seat.objects.create(
            seat_number="C1",
            status="available",
            movie=self.movie
        )
        self.url = reverse('booking-list')

    def test_get_booking_list(self):
        """Test retrieving booking list"""
        Booking.objects.create(
            movie=self.movie,
            seat=self.seat,
            user=self.user
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_booking(self):
        """Test creating a new booking"""
        data = {
            'movie': self.movie.id,
            'seat': self.seat.id,
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.count(), 1)
        # Check that seat status was updated
        self.seat.refresh_from_db()
        self.assertEqual(self.seat.status, 'booked')

    def test_create_booking_for_booked_seat(self):
        """Test creating booking for already booked seat fails"""
        self.seat.status = 'booked'
        self.seat.save()
        data = {
            'movie': self.movie.id,
            'seat': self.seat.id,
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TemplateViewTest(TestCase):
    """Integration tests for template-based views"""

    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )
        self.movie = Movie.objects.create(
            title="Template Test Movie",
            description="Testing templates",
            release_date=date(2024, 1, 1),
            duration=120
        )
        self.seat = Seat.objects.create(
            seat_number="D1",
            status="available",
            movie=self.movie
        )

    def test_movie_list_view(self):
        """Test movie list view renders correctly"""
        response = self.client.get(reverse('movie_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookings/movie_list.html')
        self.assertContains(response, "Template Test Movie")

    def test_seat_booking_view_get(self):
        """Test seat booking view renders correctly"""
        response = self.client.get(reverse('book_seat', args=[self.movie.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookings/seat_booking.html')
        self.assertContains(response, "Template Test Movie")

    def test_seat_booking_view_post(self):
        """Test booking a seat through the form"""
        response = self.client.post(
            reverse('book_seat', args=[self.movie.id]),
            {'seat_id': self.seat.id}
        )
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertEqual(Booking.objects.count(), 1)
        self.seat.refresh_from_db()
        self.assertEqual(self.seat.status, 'booked')

    def test_booking_history_view(self):
        """Test booking history view renders correctly"""
        Booking.objects.create(
            movie=self.movie,
            seat=self.seat,
            user=self.user
        )
        response = self.client.get(reverse('booking_history'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookings/booking_history.html')
        self.assertContains(response, "Template Test Movie")