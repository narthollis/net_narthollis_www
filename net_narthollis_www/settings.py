"""
Django settings for net_narthollis_www project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'vr(%avajk!11h)+k6l!*)gk6&lvq7g&j#&c-)va+&82a5ab8n_'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = False

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.sites',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.contenttypes',
    #'django.contrib.comments',

    'south',

    'zinnia_theme_netnarthollis',

    'zinnia_html5',
    # For Zinnia
    'tagging',
    'mptt',
    'zinnia',

    #'django_xmlrpc',

    #'debug_toolbar',
)

SITE_ID=1

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'net_narthollis_www.urls'

WSGI_APPLICATION = 'net_narthollis_www.wsgi.application'

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'zinnia.context_processors.version', # Optional
)

TEMPLATE_LOADERS = (
    'app_namespace.Loader',

    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',

    'django.template.loaders.eggs.Loader'
)

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-au'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

ZINNIA_WYSIWYG=False
ZINNIA_MARKUP_LANGUAGE = 'markdown'
ZINNIA_MARKDOWN_EXTENSIONS = 'extra,admonition,codehilite'

ZINNIA_AUTO_CLOSE_COMMENTS_AFTER = 0
ZINNIA_AUTO_CLOSE_PINGBACKS_AFTER = 0
ZINNIA_AUTO_CLOSE_TRACKBACKS_AFTER = 0

#from zinnia.xmlrpc import ZINNIA_XMLRPC_METHODS
#XMLRPC_METHODS = ZINNIA_XMLRPC_METHODS

from .local_settings import *
MANAGERS = ADMINS
TEMPLATE_DEBUG = DEBUG

