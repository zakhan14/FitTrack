from django.urls import path
from . import views 
from .views import custom_logout, ProgresoView

urlpatterns = [
    path('', views.index, name='index'),
    path('registro_del_entrenamiento/', views.entrenamiento, name='entrenamiento'),
    path('progreso/', ProgresoView.as_view(), name='progreso'),
    path('detalle/', views.detalle, name='detalle'),
    path('log_in/', views.log_in, name='log_in'),
    path('sign_up/', views.sign_up, name='sign_up'), 
    path('logout/', custom_logout, name='custom_logout'),
]
