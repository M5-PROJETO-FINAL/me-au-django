from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .permissions import IsAdminUser, IsAdm
from .models import Room, RoomType
from .serializers import Room_TypeSerializer, RoomSerializer
from rest_framework.generics import (
    ListCreateAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
)


class RoomView(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdm]

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
