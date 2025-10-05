from django.db import models
from django.contrib.auth.models import User


class Movie(models.Model):
    """Model representing a movie in the theater"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    release_date = models.DateField()
    duration = models.IntegerField(help_text="Duration in minutes")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['release_date']


class Seat(models.Model):
    """Model representing a seat in the theater"""
    SEAT_STATUS_CHOICES = [
        ('available', 'Available'),
        ('booked', 'Booked'),
    ]

    seat_number = models.CharField(max_length=10)
    status = models.CharField(
        max_length=20,
        choices=SEAT_STATUS_CHOICES,
        default='available'
    )
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name='seats',
        null=True,
        blank=True
    )

    def __str__(self):
        return f"Seat {self.seat_number} - {self.status}"

    class Meta:
        ordering = ['seat_number']
        unique_together = ['seat_number', 'movie']  # Unique per movie


class Booking(models.Model):
    """Model representing a booking made by a user"""
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    seat = models.ForeignKey(
        Seat,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    booking_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.movie.title} - Seat {self.seat.seat_number}"

    class Meta:
        ordering = ['-booking_date']
        unique_together = ['movie', 'seat']  # Prevent double booking same seat for same movie