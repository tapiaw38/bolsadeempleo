from django.urls import path
from service import views


urlpatterns = [
    path('lista/', views.service_list.as_view(), name='list'),
    path('new/', views.CreateService.as_view(), name = 'create'),
    path('service/<int:pk>/', views.ServiceDetail.as_view(), name = 'service_detail')
]