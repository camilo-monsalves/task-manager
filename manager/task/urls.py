from django.urls import path
# vistas (views.py)
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('registro/', views.registro, name='registro-usuario'),
    path('login/', views.login_usuario, name='login-usuario'),
    path('logout/', views.logout_usuario, name='logout-usuario'),
    path('crear-tarea/', views.crear_tarea, name='add-tarea'),
    path('ver-tareas/', views.lista_tareas, name='list-tarea'),
    path('ver-tareas/<int:tarea_id>/', views.detalle_tarea, name='detalle-tarea'),
    path('ver-tareas/eliminar/<int:pk>', views.EliminarTarea.as_view(), name='eliminar-tarea'),
    path('ver-tareas/editar/<int:pk>', views.EditarTarea.as_view(), name='editar-tarea'),
    path('ver-tareas/completar/<int:tarea_id>', views.cambiar_estado_tarea, name='cambiar-estado-tarea'),
    path('ver-tareas/observacion/<int:tarea_id>', views.crear_observacion, name='crear-observacion')
]