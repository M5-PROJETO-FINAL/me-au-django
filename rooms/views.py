from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAdminUser
from .models import Room, RoomType
from .serializers import Room_TypeSerializer, RoomSerializer
from rest_framework.generics import ListCreateAPIView


class RoomView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    serializer_class = RoomSerializer
    queryset = Room.objects.all()

    def perform_create(self, serializer):
        room_type_obj = get_object_or_404(RoomType, pk=self.kwargs.get("pk"))
        return serializer.save(room_type=room_type_obj)


class RoomTypesView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    serializer_class = Room_TypeSerializer
    queryset = RoomType.objects.all()

    def perform_create(self, serializer):
        serializer.save()
