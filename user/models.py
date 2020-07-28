from django.db import models
from django.contrib.auth.models import User
# Import image
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
# Create your models here.

class Person(models.Model):
    user = models.OneToOneField(User, blank=False, null=False, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=10,default="", blank=True, null=True,verbose_name="Número de teléfono")
    direction = models.CharField(max_length=100)
    picture = models.ImageField(upload_to="user/pictures",blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.user.username

