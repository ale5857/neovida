from django.urls import path
from . import views

app_name = 'consultas'

urlpatterns = [
path('consulta/<int:consulta_id>/', views.detalle_consulta, name='detalle_consulta')
]
