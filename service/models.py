from django.db import models
from django.contrib.auth.models import User
from user.models import Person
# Create your models here.

class Service(models.Model):
    user = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, null=False, blank=False, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    direction = models.CharField(max_length=100, null=True, blank=True)
    facebook_url = models.CharField(max_length=100, null=True, blank=True)
    picture_logo = models.ImageField(upload_to="service/pictures")
    calification = models.FloatField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '@{}, servicio: {}'.format(self.person.user.username, self.title)