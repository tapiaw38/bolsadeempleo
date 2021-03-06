from django.urls import path
from service import views


urlpatterns = [
    path('lista/', views.ServiceList.as_view(), name='list'),
    path('list_index/', views.service_index, name='list_index'),
    path('list_json/', views.service_list, name='list_json'),
    path('new/', views.service_create, name = 'create'),
    #path('images/', views.CreateImage.as_view(), name = 'create_image'),
    path('images/', views.image_service, name='image_list'),
    path('service/<int:pk>/', views.ServiceDetail.as_view(), name = 'service_detail'),
    #path('delete/<int:pk>/', views.DeleteService.as_view(), name = 'delete'),
    path("search/<str:search>/", views.category_search , name="search_category"),
    path("like/", views.like_service, name="like"),
    path("delete/", views.delete_service, name="delete"),
    path('contact/', views.contact, name='contact'),
]