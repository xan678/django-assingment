# Create your models here.

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.crypto import get_random_string

from common.models import BaseModel


class UserManager(BaseUserManager):

    def create_user(self, email, password):
        if not email:
            raise ValueError('Users must have an username.')

        user = self.model(email=email)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password):

        if password is None:
            raise ValueError('Superusers must have a password.')

        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class UserProfile(BaseModel, AbstractUser):
    """
    customizing exist user model to add extra fields
    """
    username = models.CharField(max_length=512, unique=True, blank=True, db_index=True)
    email = models.EmailField(db_index=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=15, null=True, blank=True)

    objects = UserManager()

    def _str_(self):
        return self.email

    class Meta:
        db_table = "user"
        ordering = ('first_name', 'last_name')
        verbose_name = "User"

    @property
    def full_name(self):
        return "%s %s" % (self.first_name, self.last_name)

    def save(self, *args, **kwargs):
        if self.email:
            self.email = self.email.lower()
        if not self.username:
            #username auto created
            username = self.email.lower().split('@')[0]
            if UserProfile.objects.filter(username=username).exists():
                username = username + get_random_string(length=7, allowed_chars='12345678908284474')
            else:
                username = username
            self.username = username
        super(UserProfile, self).save(*args, **kwargs)