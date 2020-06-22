from django.urls import path
from service import views


urlpatterns = [
    path('lista/', views.service_list, name='list'),
]