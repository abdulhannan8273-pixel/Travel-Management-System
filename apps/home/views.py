from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from apps.destinations.models import Destination
from apps. destinations.serializers import DestinationSerializer

class HomeAPIVies(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        featured = Destination.objects.filter(is_featured=True) [:6]
        top_rated = Destination.objects.order_by("-rating") [:6]
        latest = Destination.objects.order_by("-created_at") [:6]
        budget = Destination.objects.order_by("price") [:6]

        return Response({
            "featured_destinations": DestinationSerializer(featured, many=True).data,
            "top_rated_destinations": DestinationSerializer(top_rated, many=True).data,
            "latest_destinations": DestinationSerializer(latest, many=True).data,
            "budget_destinations": DestinationSerializer(budget, many=True).data,
        })