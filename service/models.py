from django.db import models
from django.contrib.auth.models import User
from user.models import Person
# Import image
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
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

    def save(self, *args, **kwargs):
        imageTemproary = Image.open(self.picture_logo)
        imageTemproary = imageTemproary.convert('RGB')
        outputIoStream = BytesIO()

        w, h = imageTemproary.size

        if w > 2000:
            w = int(w/4)
            h = int(h/4)

        elif h > 2000:
            w = int(w/4)
            h = int(h/4)

        elif w > 1400:
            w = int(w/3)
            h = int(h/3)

        elif h > 1400:
            w = int(w/3)
            h = int(h/3)

        elif w > 800:
            w = int(w/2)
            h = int(h/2)

        elif h > 800:
            w = int(w/2)
            h = int(h/2)

        imageTemproaryResized = imageTemproary.resize((w,h))

        imageTemproaryResized.save(outputIoStream , format='JPEG', quality=150)
        outputIoStream.seek(0)
        self.picture_logo = InMemoryUploadedFile(outputIoStream,'ImageField', "%s.jpg" %self.picture_logo.name.split('.')[0], 'image/jpeg', sys.getsizeof(outputIoStream), None)
        super(Service, self).save(*args, **kwargs)

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