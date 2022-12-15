from django.db import models
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