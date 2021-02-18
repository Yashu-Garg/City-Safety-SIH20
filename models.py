from django.db import models
from django.contrib.auth.models import (AbstractBaseUser,BaseUserManager)
from .managers import CustomUserManager
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone
# Create your models here.
GENDER_CHOICES = (
   ('M', 'Male'),
   ('F', 'Female')
)
class People(AbstractBaseUser,PermissionsMixin):
    name=models.CharField(max_length=50)
    gender = models.CharField(choices=(
   ('M', 'Male'),
   ('F', 'Female')
), max_length=128)
    ContactNumber=models.CharField(max_length=13)
    Aadhar_Number=models.CharField(max_length=12)
    EmailId=models.EmailField(unique=True)
    Age=models.IntegerField()
    RecoveryNumber=models.CharField(max_length=13)
    RecoveryMail=models.EmailField()
    Latitude=models.FloatField(default=-1)
    Longitude=models.FloatField(default=-1)
    City=models.CharField(max_length=50,default='Unknown')
    LocationDateTime=models.DateTimeField(auto_now_add=True)
    Address=models.CharField(max_length=500,default='Unknown')
    #password=models.CharField(max_length=15)
    date_created=models.DateTimeField(auto_now_add=True,auto_now=False)
    updated_at=models.DateTimeField(auto_now_add=False,auto_now=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomUserManager()
    USERNAME_FIELD = 'EmailId'
    REQUIRED_FIELDS = ['Aadhar_Number']

    def __str__(self):
        return self.EmailId



class PersonInNeed(models.Model):
    person=models.ForeignKey(People,on_delete=models.CASCADE)
    Latitude = models.FloatField(default=-1)
    Longitude = models.FloatField(default=-1)
    City = models.CharField(max_length=50, default='Unknown')
    Address = models.CharField(max_length=500, default='Unknown')
    Added_at = models.DateTimeField(auto_now_add=True)
    audio = models.FileField(upload_to='sih/audio')
    Action_taken=models.BooleanField(default=False)
    Action_taken_at=models.DateTimeField(auto_now_add=False,auto_now=True)

class Audio(models.Model):
    aud=models.FileField(upload_to='sih/static/Audio')
    name=models.CharField(max_length=50,default='ashish')