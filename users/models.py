from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
import os
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.crypto import get_random_string
from locations.models import Location  # Make sure this path is correct


# Create your models here.
class CustomUser(AbstractUser):

    STATUS = (
        ('regular', 'regular'),
        ('subscriber', 'subscriber'),
        ('moderator', 'moderator'),
    )

    email = models.EmailField(unique=True)
    status = models.CharField(max_length=100, choices=STATUS, default='regular')
    description = models.TextField("Description", max_length=600, default='', blank=True)

    def __str__(self):
        return self.username


class Contact(models.Model):
    firstname = models.CharField(max_length=122)
    lastname = models.CharField(max_length=122)
    email = models.CharField(max_length=122)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    date = models.DateField()

    def __str__(self):
        return self.firstname
    
class SubscribedUsers(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, max_length=100)
    created_date = models.DateTimeField('Date created', default=timezone.now)

    def __str__(self):
        return self.email
    


# New codes Start form here

class FaceRegistration(models.Model):
    DESIGNATION_CHOICES = [
        ('1 year', '1 year'),
        ('2 years', '2 years'),
        ('3 years', '3 years'),
    ]

    ORGANIZATION_CHOICES = [
        ('IBM', 'IBM'),
        ('Edunet', 'Edunet'),
        ('DGT', 'DGT'),
    ]

    DIVISION_UNIT_CHOICES = [
        ('ADIT', 'ADIT'),
        ('IOT', 'IOT'),
        ('CSA', 'CSA'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    designation = models.CharField(max_length=7, choices=DESIGNATION_CHOICES)
    mobile = models.CharField(max_length=15)
    organization = models.CharField(max_length=6, choices=ORGANIZATION_CHOICES)
    division_unit = models.CharField(max_length=4, choices=DIVISION_UNIT_CHOICES)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)
    private_key = models.CharField(max_length=255, blank=True)
    face_data = models.JSONField(default=dict, blank=True)
    attendance_id = models.CharField(max_length=8, unique=True, blank=True)
    aadhar_id = models.CharField(max_length=12)
    user_picture = models.ImageField(upload_to='user_pictures/', null=True, blank=True)  # New field

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        self.first_name = self.user.first_name
        self.last_name = self.user.last_name
        self.email = self.user.email

        if not self.private_key:
            self.private_key = get_random_string(64)  # Generate a random string as the private key
        if not self.face_data:
            self.face_data = {}  # Replace with your logic to generate face data
        if not self.attendance_id:
            # Generate attendance_id based on location, user's first name, last name, and email
            location_prefix = self.location.name[:3].upper() if self.location else 'UNK'
            random_numbers = get_random_string(length=5, allowed_chars='0123456789')
            self.attendance_id = f"{location_prefix}{random_numbers}"

        super().save(*args, **kwargs)