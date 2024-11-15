from django.utils import timezone
from rest_framework import status
from rest_framework import generics
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from app_accounts.models import UserModel, VerificationModel
from app_accounts.serializers import RegisterSerializers, LoginSerializer, VerificationSerializer
from .utils import sms_sender


class RegistrationView(generics.CreateAPIView):
    serializer_class = RegisterSerializers
    queryset = UserModel.objects.all()
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(serializer.validated_data['password'])
        user.is_active = False
        user.save()
        phone_number = serializer.validated_data.get('phone_number')
        message = (f"Hi {user.first_name} {user.last_name}, welcome to our website! Please verify your account."
                   f" We are sent code your email . ")

        if phone_number:
            sms_sender(phone_number, message)
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

        try:
            verification = VerificationModel.objects.get(
                code=serializer.validated_data['code']
            )
        except VerificationModel.DoesNotExist:
            return Response({"detail": "Invalid verification code."}, status=status.HTTP_400_BAD_REQUEST)

        if verification.created_at + timezone.timedelta(minutes=5) < timezone.now():
            verification.delete()
            return Response({"detail": "Verification code has expired."}, status=status.HTTP_400_BAD_REQUEST)

        user = verification.user

        if not user.is_active:
            user.is_active = True
            user.save()

        verification.delete()
        return Response({"message": "User verified successfully"})
        
class FollowView(generics.GenericAPIView):
    serializer_class = FollowSerializer
    queryset = FollowerModel.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        follower = serializer.validated_data['follower']
        following = request.user
        follow = FollowerModel.objects.filter(follower=follower, user=following)
        response = {
            'success': True,
            'message': {
                'follower': follower.username,
                'following': following.username,
                'action': 'follow' if not follow.exists() else 'unfollow'
            }

        }
        if follow.exists():
            if follow.exists():
                follow.delete()
                return Response(response, status=status.HTTP_200_OK)
        FollowerModel.objects.create(follower=follower, user=following)
        return Response(response, status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):
        follower = request.user
        following = FollowerModel.objects.filter(follower=follower)
        follow = FollowerModel.objects.filter(user=follower)
        serializer = self.get_serializer(following, many=True)
        response = {
            'success': True,
            'message': {
                'follower': follower.username,
                'following': [follow.user.username for follow in following],
                'follow': [follow.follower.username for follow in follow]
            }
        }
        return Response(response, status=status.HTTP_200_OK)
