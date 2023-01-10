from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Pet
from .serializers import PetSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdminOrPetOwner
from rest_framework.views import Response, status


class PetView(ListCreateAPIView):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_adm:
            return self.queryset.all()

        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PetDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminOrPetOwner]


    def patch(self, request, *args, **kwargs):
        
        if "type" in request.data:
            return Response({'detail': 'Type field cannot be updated'}, status=status.HTTP_400_BAD_REQUEST)

        return self.partial_update(request, *args, **kwargs)
