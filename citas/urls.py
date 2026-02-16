from django.urls import path
from . import views

app_name = 'citas'   # 👈 ESTO ES CLAVE (namespace)

urlpatterns = [
    path('', views.agenda_citas, name='agenda'),
]
