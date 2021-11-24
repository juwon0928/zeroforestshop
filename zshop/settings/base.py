import os
import dj_database_url
from decouple import config
from django.views.generic import TemplateView

from zshop.settings.development import DATABASES

import sys
sys.modules['django.utils.six.moves.urllib.parse']=__import__('six.moves.urllib_parse', fromlist=['urlencode'])
sys.modules['django.utils.six.moves.urllib.request']=__import__('six.moves.urllib_request', fromlist=['urlopen'])


BASE_DIR = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))

SECRET_KEY = config('SECRET_KEY')

DEBUG = False

# ALLOWED_HOSTS = ['127.0.0.1', '.herokuapp.com']

INSTALLED_APPS = [
    'baton',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'crispy_forms',
    'django_countries',
    'core.apps.CoreConfig',
    'django_summernote',
    'baton.autodiscover'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'zshop.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.categories',
            ],
        },
    },
]

WSGI_APPLICATION = 'zshop.wsgi.application'


LANGUAGE_CODE = 'ko-kr'
TIME_ZONE = 'Asia/Seoul'
USE_I18N = True
USE_L10N = True
USE_TZ = True


STATIC_URL = '/static/'
MEDIA_URL = '/media/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static_in_env')]
STATIC_ROOT = os.path.join(BASE_DIR, 'static_root')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media_root')


AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend'
)
SITE_ID = 1
LOGIN_REDIRECT_URL = '/'


CRISPY_TEMPLATE_PACK = 'bootstrap4'

X_FRAME_OPTIONS = 'SAMEORIGIN'

FILE_UPLOAD_HANDLERS = [
    'django.core.files.uploadhandler.MemoryFileUploadHandler',
    'django.core.files.uploadhandler.TemporaryFileUploadHandler',
]

MAX_UPLOAD_SIZE = 5242880
DATA_UPLOAD_MAX_MEMORY_SIZE = None
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880
DATA_UPLOAD_MAX_NUMBER_FIELDS = None

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

BATON = {
    'SITE_HEADER' : 'ZEROFOREST',
    'SITE_TITLE' : 'ZEROFOREST',
    'INDEX_TITLE' : 'ZEROFOREST_SHOP',
    'SUPPORT_HREF' : 'https://velog.io/@codren',
    'COPYRIGHT' : 'copyright 2021 Codren',
    'POWERED_BY' : '<a href = "https://velog.io/@codren">Codren</a>',
    'MENU_TITLE' : 'Menu',
    'MENU': (
        { 'type': 'title', 'label': 'main', 'apps': ('core', 'account', 'sites', 'socialaccount', 'auth', 'django_summernote') },
        {'type': 'app', 'name': 'core','label': '관리'},
        {'type': 'app','name': 'account','label': '계정'},
        {'type': 'app', 'name': 'sites', 'label': '사이트들'},
        {'type': 'app', 'name': 'socialaccount', 'label': '소셜 계정'},
        {'type': 'app', 'name': 'auth', 'label': '인증 및 권한'},
        {'type': 'app', 'name': 'django_summernote', 'label': '썸머노트'},
    ),}

STATIC_ROOT = os.path.join(BASE_DIR,'staticfiles')