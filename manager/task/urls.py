from django.urls import path
# vistas (views.py)
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('registro/', views.registro, name='registro-usuario'),
    path('login/', views.login_usuario, name='login-usuario'),
    path('logout/', views.logout_usuario, name='logout-usuario')
]