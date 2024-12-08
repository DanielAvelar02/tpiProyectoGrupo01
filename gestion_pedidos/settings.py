from pathlib import Path
import os
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'negocio', 'static'),
]


PWA_SERVICE_WORKER_PATH = os.path.join(BASE_DIR, 'negocio/static/js', 'serviceworker.js')

PWA_APP_NAME = 'Los3Cerditos'
PWA_APP_DESCRIPTION = "Los3Cerditos PWA"
PWA_APP_THEME_COLOR = '#000000'
PWA_APP_BACKGROUND_COLOR = '#ffffff'
PWA_APP_DISPLAY = 'standalone'
PWA_APP_SCOPE = '/'
PWA_APP_ORIENTATION = 'any'
PWA_APP_START_URL = '/'
PWA_APP_STATUS_BAR_COLOR = 'default'
PWA_APP_ICONS = [
	{
		'src': 'static/images/favicon.png',
		'sizes': '512x512'
	}
]
PWA_APP_ICONS_APPLE = [
	{
		'src': 'static/images/favicon.png',
		'sizes': '512x512'
	}
]
PWA_APP_SPLASH_SCREEN = [
	{
		'src': 'static/images/favicon.png',
		'media': '(device-width: 320px) and (device-height: 568px) and (-webkit-device-pixel-ratio: 2)'
	}
]
PWA_APP_DIR = 'ltr'
PWA_APP_LANG = 'en-US'


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-es+9xi+=h8$1o-l2e96a6plub_ko*9zqkiaox=#0hg0i02ctox'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

#Cuando la aplicacion este local, descomentar la siguiente linea
ALLOWED_HOSTS = ['127.0.0.1']

#Cuando la aplicacion este en produccion, descomentar la siguiente linea
#ALLOWED_HOSTS = ['34.72.177.176']

# settings.py
LOGIN_URL = 'login'  # Asegura que se redirija a la URL del login personalizado
LOGIN_REDIRECT_URL = '/'  # Redirige a la página de inicio después de un login exitoso
LOGOUT_REDIRECT_URL = '/' # Redirige a la página de inicio después de un logout exitoso
MEDIA_URL = '/media/' # URL de los archivos multimedia
MEDIA_ROOT = os.path.join(BASE_DIR, 'media') # Ruta de los archivos multimedia

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'negocio',
    'pwa',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'gestion_pedidos.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # Sirve para que los datos del negocio estén disponibles en todas las vistas
                'negocio.context_processors.negocio_context',  # Agrega el contexto del negocio
            ],
        },
    },
]

WSGI_APPLICATION = 'gestion_pedidos.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# No modificar esta sección-----------------------------------
# Configuración de la base de datos en desarrollo
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Configuración de la base de datos en producción
""" DATABASES = {
    'default': dj_database_url.config(
        # Replace this value with your local database's connection string.
        default='postgresql://postgres:postgres@localhost:5432/mysite',
        conn_max_age=600
    )
} """

#No modificar esta sección-----------------------------------

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'es'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
