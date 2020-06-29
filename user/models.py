from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Person(models.Model):
    user = models.OneToOneField(User, blank=False, null=False, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=10,default="", blank=True, null=True,verbose_name="Número de teléfono")
    direction = models.CharField(max_length=100)
    picture = models.ImageField(upload_to="user/pictures",blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    message = models.ManyToManyField(Person, default=None, blank=True, related_name='message')

    def __str__(self):
        return self.user.username


class Message(models.Model):
    user = models.ForeignKey(User,null=True, blank=True,on_delete=models.CASCADE)
    person = models.ForeignKey(Person,null=True, blank=True,on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'mensaje de {}'.format(self.user.username)