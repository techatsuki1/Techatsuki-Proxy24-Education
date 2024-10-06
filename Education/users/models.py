import os
import random
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.conf import settings


class CustomUser(AbstractUser):
    def image_upload_to(self, filename):
        # Construct the upload path based on user email and filename
        return os.path.join("Users", self.email, filename)

    STATUS_CHOICES = (
        ('student', 'Student'),
        ('tutor', 'tutor'),
        ('others', 'Others'),
    )
    
    GENDER_CHOICES=(
        ('male', 'Male'),
        ('female', 'Female'),
        ('others', 'Others'),
        ('prefer not to say', 'Prefer not to say'),
    )
    email = models.EmailField(unique=True)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='student')
    
    description = models.TextField("Description", max_length=600, default='', blank=True)
    image = models.ImageField(default='default/user.jpg', upload_to=image_upload_to, blank=True)
    gender = models.CharField(max_length=100, choices=GENDER_CHOICES, default="prefer not to say" ,null=True)
    designation = models.CharField(max_length=100, blank=True, null=True)

    headline = models.CharField(max_length=60, blank=True, null=True)
    language = models.CharField(max_length=20, blank=True, null=True)
    website_url = models.URLField(blank=True, null=True)
    twitter_profile = models.CharField(max_length=128, blank=True, null=True)
    facebook_profile = models.CharField(max_length=128, blank=True, null=True)
    linkedin_profile = models.CharField(max_length=128, blank=True, null=True)
    youtube_profile = models.CharField(max_length=128, blank=True, null=True)
    learning_goals = models.CharField(max_length=255, blank=True, null=True)
    experience_level = models.CharField(max_length=50, blank=True, null=True)
    skills = models.TextField(blank=True, null=True)  # You can store skills as CSV
    learning_style = models.CharField(max_length=50, blank=True, null=True)
    career_goals = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.username



