from django.urls import path
from service import views


urlpatterns = [
    path('lista/', views.ServiceList.as_view(), name='list'),
    path('new/', views.CreateService.as_view(), name = 'create'),
    path('service/<int:pk>/', views.ServiceDetail.as_view(), name = 'service_detail'),
    path("search/<str:search>/", views.category_search , name="search_category"),
    path("like/", views.like_service, name="like"),
    path("message/", views.CreateMessage.as_view(), name="message"),
]