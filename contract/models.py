from django.db import models
from user.models import Person
from service.models import Service
# Create your models here.

class Contract(models.Model):
    person = models.ForeignKey(Person, null=False, blank=False, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, null=False, blank=False, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)