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
    direction = models.CharField(max_length=100,blank=True, null=True)
    picture = models.ImageField(upload_to="user/pictures",blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        if self.picture:
            imageTemproary = Image.open(self.picture)
            imageTemproary = imageTemproary.convert('RGB')
            outputIoStream = BytesIO()

            w, h = imageTemproary.size

            if w > 1400 and h > 1400:
                w = int(w/3)
                h = int(h/3)
            elif w > 600 and h > 600:
                w = int(w/2)
                h = int(h/2)



            imageTemproaryResized = imageTemproary.resize((w,h)) 

            imageTemproaryResized.save(outputIoStream , format='JPEG', quality=150)
            outputIoStream.seek(0)
            self.picture = InMemoryUploadedFile(outputIoStream,'ImageField', "%s.jpg" %self.picture.name.split('.')[0], 'image/jpeg', sys.getsizeof(outputIoStream), None)
        super(Person, self).save(*args, **kwargs)