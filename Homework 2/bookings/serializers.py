from rest_framework import serializers
from .models import Movie, Seat, Booking
from django.contrib.auth.models import User


class MovieSerializer(serializers.ModelSerializer):
    """Serializer for Movie model"""

    class Meta:
        model = Movie
        fields = ['id', 'title', 'description', 'release_date', 'duration']
        read_only_fields = ['id']


class SeatSerializer(serializers.ModelSerializer):
    """Serializer for Seat model"""
    movie_title = serializers.CharField(source='movie.title', read_only=True)

    class Meta:
        model = Seat
        fields = ['id', 'seat_number', 'status', 'movie', 'movie_title']
        read_only_fields = ['id']


class BookingSerializer(serializers.ModelSerializer):
    """Serializer for Booking model"""
    movie_title = serializers.CharField(source='movie.title', read_only=True)
    seat_number = serializers.CharField(source='seat.seat_number', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Booking
        fields = ['id', 'movie', 'movie_title', 'seat', 'seat_number',
                  'user', 'username', 'booking_date']
        read_only_fields = ['id', 'booking_date', 'user']

    def validate(self, data):
        """Validate that the seat is available and belongs to the movie"""
        seat = data.get('seat')
        movie = data.get('movie')

        # Check if seat is available
        if seat.status == 'booked':
            raise serializers.ValidationError("This seat is already booked.")

        # Check if seat belongs to the movie (if seat has a movie assigned)
        if seat.movie and seat.movie != movie:
            raise serializers.ValidationError("This seat is not available for this movie.")

        return data

    def create(self, validated_data):
        """Create booking and update seat status"""
        seat = validated_data['seat']

        # Mark seat as booked
        seat.status = 'booked'
        seat.movie = validated_data['movie']
        seat.save()

        # Create the booking
        booking = Booking.objects.create(**validated_data)
        return booking


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model (for reference)"""

    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        read_only_fields = ['id']