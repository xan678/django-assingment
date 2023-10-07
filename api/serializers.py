from rest_framework import serializers

from api.models import Post
from user.serializers import UserProfileShortSerializer


class PostSerializer(serializers.ModelSerializer):
    user = UserProfileShortSerializer(read_only=True)

    class Meta:
        model = Post
        fields = "__all__"
