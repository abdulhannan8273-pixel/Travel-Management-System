from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import Country, State, City
from .serializers import (CountrySerializer, StateSerializer, CitySerializer)
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from .serializers import CSVUploadSerializer
from .csv_import import (import_countries, import_states, import_cities,)


class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [AllowAny]


class StateViewSet(viewsets.ModelViewSet):
    queryset = State.objects.all()
    serializer_class = StateSerializer
    permission_classes = [AllowAny]
    

class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [AllowAny]

class CountryCSVImportView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = CSVUploadSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        file = serializer.validated_data.get("file")

        if file is None:
            return Response({"error": "File is required."}, status=400)

        return import_countries(file)
    

class StateCSVImportView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = CSVUploadSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        file = serializer.validated_data.get("file")

        return import_states(file)
    
class CityCSVImportView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = CSVUploadSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        file = serializer.validated_data.get("file")

        return import_cities(file)