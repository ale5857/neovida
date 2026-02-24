from django.urls import path
from . import views

app_name = 'expedientes'

urlpatterns = [
    path('ver/<int:paciente_id>/', views.ver_expediente, name='ver_expediente'),
    path('completo/<int:paciente_id>/', views.expediente_completo, name='expediente_completo'),
    path(
    'consulta/crear/<int:expediente_id>/',
    views.crear_consulta_prenatal,
    name='crear_consulta_prenatal'),

    path('embarazo/finalizar/<int:embarazo_id>/', views.finalizar_embarazo, name='finalizar_embarazo'),
    path('embarazo/nuevo/<int:expediente_id>/', views.nuevo_embarazo, name='nuevo_embarazo'),



]
