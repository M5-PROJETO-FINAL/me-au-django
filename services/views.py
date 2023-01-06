from .models import  Service
from .serializers import ServiceSerializer
from rest_framework.generics import ListCreateAPIView


class ServiceView(ListCreateAPIView):
    
    serializer_class = ServiceSerializer
    queryset = Service.objects.all()

    def perform_create(self, serializer):
         serializer.save()
