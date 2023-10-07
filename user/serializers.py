from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from user.models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(max_length=256, write_only=True)

    class Meta:
        model = UserProfile
        fields = ('id', 'email', 'first_name', 'last_name', 'password', 'confirm_password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        if (validated_data['password']) != validated_data['confirm_password']:
            raise serializers.ValidationError(detail={"password": ["Please check the password you've entered"]})

        validated_data.pop('confirm_password')
        validated_data['password'] = make_password(validated_data['password'])
        return super(UserProfileSerializer, self).create(validated_data)


class UserProfileShortSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ('id', 'first_name', 'last_name', 'username')


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=256)
