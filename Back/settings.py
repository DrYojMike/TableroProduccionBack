from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
from pathlib import Path
from dotenv import load_dotenv
import os

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")
# ========================
# SEGURIDAD
# ========================
SECRET_KEY = 'django-insecure-&&(v@)#7!-r1u=+=3x^j089lpjwh88%musxr0$6*zl1s2)*x!l'
DEBUG = True

ALLOWED_HOSTS = ['*']


# ========================
# APLICACIONES
# ========================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'corsheaders',

    'clientes',
    'pedidos',
    'op',
]


# ========================
# MIDDLEWARE
# ========================
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # IMPORTANTE
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# ========================
# URLS / TEMPLATES
# ========================
ROOT_URLCONF = 'Back.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Back.wsgi.application'


# ========================
# BASES DE DATOS
# ========================
from pathlib import Path
from dotenv import load_dotenv
import os
DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE'),
        'NAME': os.getenv('DB_NAME_DEFAULT'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
        'OPTIONS': {
            'driver': os.getenv('DB_DRIVER'),
        }
    },

    'facturacion': {
        'ENGINE': os.getenv('DB_ENGINE'),
        'NAME': os.getenv('DB_NAME_FACTURACION'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
        'OPTIONS': {
            'driver': os.getenv('DB_DRIVER'),
        }
    },

    'inventario': {
        'ENGINE': os.getenv('DB_ENGINE'),
        'NAME': os.getenv('DB_NAME_INVENTARIO'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
        'OPTIONS': {
            'driver': os.getenv('DB_DRIVER'),
        }
    },

    'usuarios': {
        'ENGINE': os.getenv('DB_ENGINE'),
        'NAME': os.getenv('DB_NAME_USUARIOS'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
        'OPTIONS': {
            'driver': os.getenv('DB_DRIVER'),
        }
    },
}


# ========================
# PASSWORDS
# ========================
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
]


# ========================
# INTERNACIONALIZACIÓN
# ========================
LANGUAGE_CODE = 'es-co'

TIME_ZONE = 'America/Bogota'

USE_I18N = True
USE_TZ = True


# ========================
# STATIC FILES
# ========================
STATIC_URL = 'static/'


# ========================
# DJANGO REST FRAMEWORK
# ========================
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ]
}


# ========================
# CORS (CLAVE PARA FRONTEND)
# ========================

# Para desarrollo (abre todo)
CORS_ALLOW_ALL_ORIGINS = True

# Si quieres restringir (mejor práctica)
# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:3000",
# ]

CORS_ALLOW_CREDENTIALS = True


# ========================
# CSRF (IMPORTANTE PARA POST)
# ========================
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:3000",
]