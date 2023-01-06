from .models import  Service
from .serializers import ServiceSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView,ListAPIView
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from .permissions import IsAccountOwner, IsAdm
from rest_framework.views import Response, status
from django.shortcuts import get_object_or_404


class ServiceView(ListCreateAPIView):
    
    serializer_class = ServiceSerializer
    queryset = Service.objects.all()

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdm]

    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_classes = [AllowAny]
        return [permission() for permission in self.permission_classes]
        


class ServiceDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAccountOwner | IsAdm]

