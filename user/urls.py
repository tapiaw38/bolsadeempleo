from django.urls import path
from user import views


urlpatterns = [
    path('ingresar/',views.log_in, name='log_in'),
    path('registrarse/',views.sign_up, name='sign_up'),
    path('salir/',views.log_out, name='log_out'),
    path('mi/perfil/',views.update_person, name='update_person'),
    path('<str:username>/', views.UserDetailView.as_view(), name='detail')
]