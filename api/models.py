from django.db import models
from user.models import UserProfile
from common.models import BaseModel


class Post(BaseModel):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to="posts/images/", blank=True, null=True)
