from django.contrib import admin
from service.models import Service, Like, Message
# Register your models here.
admin.site.register(Service)
admin.site.register(Like)
admin.site.register(Message)