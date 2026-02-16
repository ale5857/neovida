from django.urls import path
from .views import panel_principal

urlpatterns = [
    path('panel/', panel_principal, name='panel_principal'),
]
