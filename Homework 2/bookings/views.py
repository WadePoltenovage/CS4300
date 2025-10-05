from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Movie, Seat, Booking
from .serializers import MovieSerializer, SeatSerializer, BookingSerializer


class MovieViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Movie model - handles CRUD operations
    """
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    @action(detail=True, methods=['get'])
    def seats(self, request, pk=None):
        """Get all seats for a specific movie"""
        movie = self.get_object()
        seats = Seat.objects.filter(movie=movie)
        serializer = SeatSerializer(seats, many=True)
        return Response(serializer.data)


class SeatViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Seat model - handles seat availability and booking
    """
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer

    @action(detail=False, methods=['get'])
    def available(self, request):
        """Get all available seats"""
        available_seats = Seat.objects.filter(status='available')
        serializer = self.get_serializer(available_seats, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def book(self, request, pk=None):
        """Book a specific seat"""
        seat = self.get_object()

        if seat.status == 'booked':
            return Response(
                {'error': 'This seat is already booked'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Update seat status
        seat.status = 'booked'
        seat.save()

        serializer = self.get_serializer(seat)
        return Response(serializer.data)


class BookingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Booking model - handles booking creation and history
    """
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def get_queryset(self):
        """Filter bookings by user if user parameter is provided"""
        queryset = Booking.objects.all()
        user_id = self.request.query_params.get('user', None)
        if user_id is not None:
            queryset = queryset.filter(user_id=user_id)
        return queryset

    def perform_create(self, serializer):
        """Set the user when creating a booking"""
        # For now, use the first user or authenticated user
        # In production, use request.user
        from django.contrib.auth.models import User
        user = self.request.user if self.request.user.is_authenticated else User.objects.first()
        serializer.save(user=user)

    @action(detail=False, methods=['get'])
    def my_bookings(self, request):
        """Get bookings for the current user"""
        if request.user.is_authenticated:
            bookings = Booking.objects.filter(user=request.user)
            serializer = self.get_serializer(bookings, many=True)
            return Response(serializer.data)
        return Response(
            {'error': 'Authentication required'},
            status=status.HTTP_401_UNAUTHORIZED
        )


# Template-based views (for the web interface)
def movie_list(request):
    """Display list of all movies"""
    movies = Movie.objects.all()
    return render(request, 'bookings/movie_list.html', {'movies': movies})


def seat_booking(request, movie_id):
    """Display seat booking page for a specific movie"""
    movie = get_object_or_404(Movie, id=movie_id)

    if request.method == 'POST':
        seat_id = request.POST.get('seat_id')
        seat = get_object_or_404(Seat, id=seat_id)

        # Get or create a default user for demo purposes
        user = request.user if request.user.is_authenticated else User.objects.first()

        if seat.status == 'available':
            # Create booking
            Booking.objects.create(
                movie=movie,
                seat=seat,
                user=user
            )
            # Update seat status
            seat.status = 'booked'
            seat.movie = movie
            seat.save()

            messages.success(request, f'Successfully booked seat {seat.seat_number} for {movie.title}!')
            return redirect('booking_history')
        else:
            messages.error(request, 'This seat is already booked.')

    # Get all seats for this movie
    seats = Seat.objects.filter(movie=movie) | Seat.objects.filter(movie__isnull=True)

    return render(request, 'bookings/seat_booking.html', {
        'movie': movie,
        'seats': seats
    })


def booking_history(request):
    """Display booking history for the current user"""
    if request.user.is_authenticated:
        bookings = Booking.objects.filter(user=request.user)
    else:
        bookings = Booking.objects.all()  # Show all for demo purposes
    return render(request, 'bookings/booking_history.html', {'bookings': bookings})