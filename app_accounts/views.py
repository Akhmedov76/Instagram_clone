from rest_framework import status
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from app_accounts.models import UserModel
from app_accounts.serializers import RegisterSerializers, LoginSerializer, VerificationSerializer


class RegistrationView(generics.CreateAPIView):
    serializer_class = RegisterSerializers
    queryset = UserModel.objects.all()
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(serializer.validated_data['password'])
        user.is_active = False
        user.save()
        return user


class LoginView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        refresh = RefreshToken.for_user(user=serializer.validated_data['user'])

        response = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "message": "Logged in successfully",
        }

        return Response(response, status=status.HTTP_200_OK)


class VerificationView(APIView):
    permission_classes = [AllowAny]
    serializer_class = VerificationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_code = serializer.validated_data.get('user_code')
        if not user_code:
            return Response({"detail": "user_code is required."}, status=status.HTTP_400_BAD_REQUEST)

        user = user_code.user
        user.is_active = True
        user.save()
        user_code.delete()
        return Response({"message": "User verified successfully"})
