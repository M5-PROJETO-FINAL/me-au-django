from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView, Response, status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import User
from .serializers import UserSerializer
from .permissions import IsAccountOwner, IsAdm
import random
from django.core.mail import send_mail
from django.conf import settings


class UserView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAccountOwner, IsAdm]


class ForgotView(APIView):
    def post(self, request):
        user = get_object_or_404(User, password_reset_code=request.data["code"])
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        user = get_object_or_404(User, email=request.data["email"])
        code = random.randint(1000, 9999)

        # se o código já existe no banco, gerar um novo
        while User.objects.filter(password_reset_code=code).exists():
            code = random.randint(1000, 9999)

        user.password_reset_code = code
        send_mail(
            subject="Your password reset code",
            message=f"Your password reset code: {code}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[request.data["email"]],
            fail_silently=False,
        )
        user.save()
        return Response({"code": code}, status=status.HTTP_200_OK)


class PasswordResetView(APIView):
    def patch(self, request, code):
        if request.data["new_password"] != request.data["confirm_password"]:
            return Response(
                {"message": "Passwords do not match"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = get_object_or_404(User, password_reset_code=code)
        user.set_password(request.data["new_password"])
        user.password_reset_code = None
        user.save()
        return Response(
            {"message": "Password reset successful"}, status=status.HTTP_200_OK
        )
