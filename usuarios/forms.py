from django import forms
from .models import Usuario
import secrets

class CrearUsuarioForm(forms.ModelForm):

    class Meta:
        model = Usuario
        fields = ['username', 'first_name', 'last_name', 'email', 'rol']

    def generar_password(self):
        return secrets.token_urlsafe(8)
