from django.contrib.auth.models import User, AbstractUser
from django.db import models

from phonenumber_field.formfields import PhoneNumberField


class UserProfile(AbstractUser):
    avatar = models.ImageField(null=True)
    phone = PhoneNumberField()

    def __str__(self):
        return self.user.username
