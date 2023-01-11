from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import Response, status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .permissions import IsAdminUser, IsAdm
from .models import Room, RoomType
from .serializers import Room_TypeSerializer, RoomSerializer
from .aux_functions.dates import get_min_and_max_dates, get_dates_in_range
from .aux_functions.availability import (
    get_all_reservations_dates_of_a_given_room_type, 
    get_all_reservations_of_a_given_room_type, 
    get_shared_room_population,
    exists_available_room
)
from rest_framework.generics import (
    ListCreateAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.views import APIView


class RoomView(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdm]

    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class RoomCreateView(ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def perform_create(self, serializer):
        room_type_obj = get_object_or_404(RoomType, pk=self.kwargs.get("pk"))
        return serializer.save(room_type=room_type_obj)


class RoomDetailView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    lookup_url_kwarg = "pk"


class RoomTypesView(ListCreateAPIView):
    queryset = RoomType.objects.all()
    serializer_class = Room_TypeSerializer

    authentication_classes = [JWTAuthentication]

    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminUser]

    def perform_create(self, serializer):
        serializer.save()


class RoomTypeDetailView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    queryset = RoomType.objects.all()
    serializer_class = Room_TypeSerializer
    lookup_url_kwarg = "pk"


class RoomDateTypeView(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminUser]

    queryset = Room.objects.all()
    lookup_url_kwarg = "pk"

    def list(self, request, pk=None):
        return Response(get_all_reservations_dates_of_a_given_room_type(pk), status=status.HTTP_200_OK)
    

class RoomDatesView(APIView):

    def get(self, request, pk):
        room_type = get_object_or_404(RoomType, pk=pk)
        room_type_reservations = get_all_reservations_of_a_given_room_type(pk)
        min_checkin, max_checkout = get_min_and_max_dates(room_type_reservations)
        all_dates = get_dates_in_range(min_checkin, max_checkout)

        # para o quarto compartilhado:
        if room_type.title == 'Quarto Compartilhado':
            result = [date for date in all_dates if get_shared_room_population(date) >= room_type.capacity]
        else:
            result = [date for date in all_dates if not exists_available_room(date, pk)]
        return Response(result, status=status.HTTP_200_OK)

    