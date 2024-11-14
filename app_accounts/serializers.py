from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from djoser.serializers import UserCreateSerializer, UserSerializer
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError

from app_accounts.models import UserModel

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


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'username', 'email', 'password')


class CustomUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = User
        fields = ('id', 'username', 'email')
