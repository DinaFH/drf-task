from django.db import models
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

  class Meta:
    verbose_name = 'user'
    verbose_name_plural = 'users'

  TYPES = (
        ('admin', 'Admin'),
        ('employee', 'Employee'),
        ('client', 'Client'),
     )
  GENDER = (
        ('m', 'Male'),
        ('f', 'Female'),
    )


  type = models.fields.CharField(verbose_name="User Type", choices=TYPES, max_length=10)
  gender = models.fields.CharField(verbose_name="Gender", choices=GENDER, max_length=1)
  date_of_birth = models.fields.DateField(verbose_name="Date of Birth")
  REQUIRED_FIELDS = ['email', 'password', 'gender', 'type', 'date_of_birth']


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)

    send_mail(
        # title:
        "Password Reset for {title}".format(title="Some website title"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email]
    )