from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Pet
from .serializers import PetSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdminOrPetOwner



class PetView(ListCreateAPIView):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


    def get_queryset(self):
        if self.request.user.is_adm:
            return self.queryset.all()

        return self.queryset.filter(user_id=self.request.user)


    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)


class PetDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminOrPetOwner]