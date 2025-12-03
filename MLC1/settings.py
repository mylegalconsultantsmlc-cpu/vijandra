import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# ------------------------
# Security
# ------------------------
SECRET_KEY = 'your-real-generated-secret-key'
DEBUG = False

ALLOWED_HOSTS = [
    'mylegalconsultants.com',
    'www.mylelegalconsultants.com',
    'mylegalconsultants.onrender.com',
    'www.mylegalconsultants.onrender.com',
    'localhost',
    '127.0.0.1',
]

CSRF_TRUSTED_ORIGINS = [
    'https://mylegalconsultants.com',
    'https://www.mylegalconsultants.com',
    'https://mylegalconsultants.onrender.com',
]

# ------------------------
# Installed Apps
# ------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Cloudinary
    'cloudinary',
    'cloudinary_storage',

    'core',
]

# ------------------------
# Middleware
# ------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # MUST stay here

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ------------------------
# URL & WSGI
# ------------------------
ROOT_URLCONF = 'MLC1.urls'
WSGI_APPLICATION = 'MLC1.wsgi.application'

# ------------------------
# Templates
# ------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'core/templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.user_flags',
                'core.context_processors.footer_settings',
            ],
        },
    },
]

# ------------------------
# Database
# ------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ------------------------
# Password validation
# ------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 'OPTIONS': {'min_length': 8}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ------------------------
# Internationalization
# ------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

# ------------------------
# Static Files
# ------------------------
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# ------------------------
# CLOUDINARY CONFIG
# ------------------------
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'dc0ucrbt8',
    'API_KEY': '979711746737173',
    'API_SECRET': 'qmVp20m1Xbp4EDQIh_R0IQtk_Do',
}

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# MEDIA URL still required but Cloudinary handles storage
MEDIA_URL = '/media/'

# ------------------------
# Custom User Model
# ------------------------
AUTH_USER_MODEL = 'core.User'

# ------------------------
# Authentication Redirects
# ------------------------
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# ------------------------
# Messages Framework
# ------------------------
from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.DEBUG: 'debug',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',
}

# ------------------------
# Email (Gmail SMTP)
# ------------------------
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'mylegalconsultants.mlc@gmail.com'
EMAIL_HOST_PASSWORD = 'jmns sbci fiwb gcuu'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# ------------------------
# Security (Production)
# ------------------------
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# ------------------------
# Default PK Field
# ------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
