from django.db import migrations

def limpiar_duplicados(apps, schema_editor):
    Usuario = apps.get_model('usuarios', 'Usuario')

    emails = {}
    for u in Usuario.objects.all():
        if u.email in emails:
            # hace el email único automáticamente
            u.email = f"{u.username}_{u.id}@temporal.com"
            u.save()
        else:
            emails[u.email] = u.id

class Migration(migrations.Migration):

    dependencies = [
    ('usuarios', '0003_alter_usuario_is_active'),
]

    operations = [
        migrations.RunPython(limpiar_duplicados),
    ]