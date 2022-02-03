from django.contrib.auth.models import AbstractUser

from phonenumber_field.modelfields import PhoneNumberField

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    phone_number = PhoneNumberField(
        verbose_name='Phone Number',
        unique=True,
    )

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return str(self.phone_number)
