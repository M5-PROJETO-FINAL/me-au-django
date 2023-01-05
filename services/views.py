from .models import  Service
from .serializers import ServiceSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView,ListAPIView
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from .permissions import IsAccountOwner, IsAdm
from django.shortcuts import get_object_or_404


class ServiceView(ListCreateAPIView):
    
    serializer_class = ServiceSerializer
    queryset = Service.objects.all()


class ListServiceView(ListAPIView):
    queryset = Service.objects.order_by()
    serializer_class = ServiceView

class ServiceDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAccountOwner]

    def delete(self, request, service_id):
        service = get_object_or_404("services.Service", id=service_id)
        service.save()
        return service
