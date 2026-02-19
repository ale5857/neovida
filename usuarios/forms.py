from django import forms
from .models import Usuario
import secrets

class CrearUsuarioForm(forms.ModelForm):

    class Meta:
        model = Usuario
        fields = ['username', 'first_name', 'last_name', 'email', 'rol']

    # generar contraseña automática
    def generar_password(self):
        return secrets.token_urlsafe(8)

    # 🔐 email obligatorio y único
def clean_email(self):
    email = self.cleaned_data.get('email')

    if not email:
        raise forms.ValidationError("El correo es obligatorio para recuperación de contraseña")

    # excluir el mismo usuario al editar
    qs = Usuario.objects.filter(email=email)
    if self.instance.pk:
        qs = qs.exclude(pk=self.instance.pk)

    if qs.exists():
        raise forms.ValidationError("Ya existe un usuario con este correo")

    return email