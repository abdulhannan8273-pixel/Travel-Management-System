from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Booking
from .serializers import BookingSerializer
from decimal import Decimal


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]
   
    def perform_create(self, serializer):
        destination = serializer.validated_data["destination"]
        people = serializer.validated_data["number_of_people"]

        total = Decimal(destination.price) * people

        serializer.save(
            user=self.request.user,
            total_price=total
        )