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
    liked = models.ManyToManyField(Person, default=None, blank=True, related_name='liked')
    created_like = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '@{}, servicio: {}'.format(self.person.user.username, self.title)

    @property
    def num_likes(self):
        return self.liked.all().count()

LIKE_CHOICES = (
    ('Like','Like'),
    ('Unlike','Unlike'),
)

class Like(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    person = models.ForeignKey(Person,null=True, blank=True,on_delete=models.CASCADE)
    service = models.ForeignKey(Service,on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES, default='Like', max_length=10)

    def __str__(self):
        return str(self.service)



"""
class Post(models.Model):
    title = models.CharField(max_length=150)
    body = models.TextField()
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    liked = models.ManyToManyField(Person, default=None, blank=True, related_name='liked')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Person, on_delete=models.CASCADE,related_name='author')

    def __str__(self):
        return self.title
    
    @property
    def num_likes(self):
        return self.liked.all().count()
"""