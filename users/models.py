from django.contrib.auth.models import AbstractUser
from django.db import models
from django.shortcuts import reverse
from django.utils.html import mark_safe
from authemail.models import EmailUserManager, EmailAbstractUser
# Create your models here.
class CustomUser(EmailAbstractUser):
    username = models.SlugField(max_length=50)
    age=models.PositiveIntegerField(null=True,blank=True)
    user_flair = models.CharField(null=True,blank=True,max_length=50)
    can_upload_images = models.BooleanField(default=True)
    objects=EmailUserManager()
