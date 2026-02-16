from django.urls import path
from . import views
from .views import agregar_paciente

app_name = 'pacientes'  # 👈 IMPORTANTE

urlpatterns = [
    path('crear/', agregar_paciente, name='agregar_paciente'),
    path('lista/', views.lista_pacientes, name='lista_pacientes'),
    path('borrar/<int:paciente_id>/', views.borrar_paciente, name='borrar_paciente'),
    path('panel/', views.panel_paciente, name='panel_paciente'),
    path('logout/', views.logout_view, name='logout'),

]
