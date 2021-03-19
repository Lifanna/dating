from django.db import models
from django.contrib.auth.models import AbstractUser, User
from . import constants as const


class Language(models.Model):
    name = models.CharField(max_length=30, blank=True)

    is_deleted = models.BooleanField(default=False)


class City(models.Model):
    name = models.CharField(max_length=30, blank=True)

    is_deleted = models.BooleanField(default=False)


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    external_id = models.CharField("External identificator", max_length=100)

    first_name = models.CharField("First name", max_length=100)

    last_name = models.CharField("Last name", max_length=100)

    gender = models.CharField("Gender", max_length=1, choices=const.GENDER, blank=True, default="")

    city = models.ForeignKey(City, on_delete=models.CASCADE)

    location = models.CharField("Location", max_length=30, blank=True)

    birth_date = models.DateField("Date of birth", blank=True, null=True)

    avatar = models.ImageField(upload_to='content', blank=True, null=True)

    # last_activity = models.DateTimeField("LastActivity", blank=True, null=True)
    
    language = models.ManyToManyField(Language)

    latitude = models.FloatField("Latitude")

    longitude = models.FloatField("Longitude")

    breefly = models.TextField("Breefly")

    is_deleted = models.BooleanField(default=False)
