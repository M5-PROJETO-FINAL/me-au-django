from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView, Response, status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import Request, Response, APIView, status
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import User
from .serializers import UserSerializer
from .permissions import IsAccountOwner, IsAdm
import random
from django.core.mail import send_mail
from django.conf import settings


class UserView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_adm:
            return self.queryset.all()

        return self.queryset.filter(email=self.request.user.email)

    def get_permissions(self):
        if self.request.method == "POST":
            self.permission_classes = [AllowAny]
        return [permission() for permission in self.permission_classes]

    # sobrescrevendo esse método para que, quando o request seja feito por um usuário não adm,
    # seja retornado apenas o objeto (não um array) // 3 últimas linhas da função
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        if request.user.is_adm:
            return Response(serializer.data)
        return Response(serializer.data[0])


class UserDetailView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAccountOwner | IsAdm]

    def patch(self, request, *args, **kwargs):

        if "is_adm" in request.data:
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN,
            )

        return self.partial_update(request, *args, **kwargs)


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
