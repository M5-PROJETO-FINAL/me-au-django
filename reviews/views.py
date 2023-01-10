from .models import Reviews
from .serializers import ReviewSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from users.permissions import IsAdm
from .permissions import IsAccountOwnerReview
from django.shortcuts import get_object_or_404


from reservations.models import Reservation


class ReviewView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = ReviewSerializer
    queryset = Reviews.objects.all()

    def perform_create(self, serializer):
        reservation = get_object_or_404(
            Reservation, pk=self.request.data["reservation_id"]
        )
        serializer.save(user=self.request.user, reservation=reservation)


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdm, IsAccountOwnerReview]

    serializer_class = ReviewSerializer
    queryset = Reviews.objects.all()
