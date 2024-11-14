from django.utils import timezone

from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from rest_framework.exceptions import ValidationError

from app_accounts.models import UserModel, VerificationModel

User = get_user_model()


class RegisterSerializers(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, max_length=50)

    class Meta:
        model = UserModel
        fields = ('id', 'first_name', 'last_name', 'username', 'email', 'password', 'confirm_password')
        extra_kwargs = {'password': {'write_only': True},
                        'first_name': {'required': False},
                        'last_name': {'required': False}
                        }

    def validate_email(self, email):
        if not email.endswith('@gmail.com') or email.count('@') != 1:
            raise serializers.ValidationError('Invalid email address.')
        return email

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')
        if password != confirm_password:
            raise serializers.ValidationError('Passwords do not match.')
        try:
            validate_password(password=password)
        except ValidationError as e:
            raise serializers.ValidationError(e)
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password', None)
        password = validated_data.get('password')
        user = UserModel.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()
        return instance


class VerificationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=4)

    class Meta:
        model = VerificationModel
        fields = ('id', 'email', 'code')

    def validate(self, attrs):
        try:
            verification = VerificationModel.objects.get(user__email=attrs['email'], code=attrs['code'])
        except VerificationModel.DoesNotExist:
            raise ValidationError("Invalid verification code.")

        if verification.created_at + timezone.timedelta(minutes=5) < timezone.now():
            verification.delete()
            raise serializers.ValidationError('Verification code has expired.')
        attrs['verification'] = verification
        return attrs


class LoginSerializer(serializers.ModelSerializer):
    email_or_username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128)
    error_messages = 'Email or username or password are required fields'

    class Meta:
        model = UserModel
        fields = ('email_or_username', 'password',)

    def validate(self, attrs):
        email_or_username = attrs.get('email_or_username')

        try:
            if email_or_username.endswith('@gmail.com'):
                user = UserModel.objects.get(email=email_or_username)
            else:
                user = UserModel.objects.get(username=email_or_username)
        except UserModel.DoesNotExist:
            raise serializers.ValidationError(self.error_messages)

        authenticated_user = authenticate(username=user.username, password=attrs.get('password'))

        if not authenticated_user:
            raise serializers.ValidationError(self.error_messages)

        attrs['user'] = user
        return attrs
