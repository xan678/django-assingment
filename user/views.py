from django.db import transaction
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny

from common.views import PostCreateModelMixin, success_response
from user.models import UserProfile
from user.serializers import UserProfileSerializer, LoginSerializer
from user.utils import create_jwt_token


# Create your views here.

class AccountView(PostCreateModelMixin, GenericAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = (AllowAny,)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        user_data = self.create(request, *args, **kwargs).data['data']
        user = UserProfile.objects.get(email=user_data['email'])
        token = create_jwt_token(user)
        return success_response(data=user_data, message="Account created", status_code=status.HTTP_201_CREATED,
                                extra_data={'token': token})


class LoginView(GenericAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        email = request.data['email']
        password = request.data['password']

        user = self.get_queryset().filter(email=email).first()
        if user and user.check_password(password):
            user_data = UserProfileSerializer(user, context={'request': request}).data
            token = create_jwt_token(user)
            return success_response(data=user_data, message="Login Successful", extra_data={'token': token})
        raise ValidationError(detail={"email": ["invalid credentials"]})
