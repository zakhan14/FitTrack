from django.urls import path
from . import views 

urlpatterns = [
    path('', views.index, name='index'),
    path('registro_del_entrenamiento/', views.entrenamiento, name='entrenamiento'),
    path('progreso/', views.progreso, name='progreso'),
    path('detalle/', views.detalle, name='detalle'),
    path('log_in/', views.log_in, name='log_in'),
    path('sign_up/', views.sign_up, name='sign_up'),  # corregido aquí
]
