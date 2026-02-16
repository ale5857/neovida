"""
Django settings for NeoVida project.
"""
import dj_database_url
import os
from pathlib import Path

# ======================
# BASE
# ======================
BASE_DIR = Path(__file__).resolve().parent.parent


# ======================
# SECURITY
# ======================
SECRET_KEY = 'django-insecure-_hgu7ed)i*!n=l^-kvd#0std-8w%!&2u0&jxt)x*we01*gug!n'
DEBUG = True
ALLOWED_HOSTS = ['neovida.onrender.com']


# ======================
# APPLICATIONS
# ======================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'usuarios',
    'pacientes.apps.PacientesConfig',
    'expedientes.apps.ExpedientesConfig',
    'consultas',
    'citas',
    'catalogos',
    'dashboard',
]

AUTH_USER_MODEL = 'usuarios.Usuario'


# ======================
# MIDDLEWARE
# ======================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# ======================
# URLS / WSGI
# ======================
ROOT_URLCONF = 'NeoVida.urls'
WSGI_APPLICATION = 'NeoVida.wsgi.application'


# ======================
# TEMPLATES
# ======================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # 👈 templates/base.html
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# ======================
# DATABASE
# ======================
DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///' + str(BASE_DIR / "db.sqlite3"),
        conn_max_age=600
    )
}


# ======================
# AUTH / LOGIN
# ======================

LOGIN_REDIRECT_URL = 'panel_principal'
LOGIN_URL = 'usuarios:login'
LOGOUT_REDIRECT_URL = 'usuarios:login'



# ======================
# PASSWORD VALIDATION
# ======================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# ======================
# INTERNATIONALIZATION
# ======================
LANGUAGE_CODE = 'es'
TIME_ZONE = 'America/Managua'
USE_I18N = True
USE_TZ = True


# ======================
# STATIC & MEDIA (🔥 CLAVE DEL PROBLEMA)
# ======================
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / 'static',  # 👈 DONDE ESTÁ css/sidebar.css
]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# ======================
# DEFAULT PK
# ======================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

import os

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'