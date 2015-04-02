"""
Django settings for stitchpick project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/(os.path.dirname(BASE_DIR)
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '$qx1vn6ba!lh5-b*ur^%etk77ki0=g(9#-tf&w8lq^0!b8r-zo'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'stitchpick',
    'login',
    'image_manipulation',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'stitchpick.urls'

WSGI_APPLICATION = 'stitchpick.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'stitchpick',
        'USER': 'postgres',
        'PASSWORD': 'x0password0x',
        'HOST': 'localhost',
        'PORT': '',
    }
}

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
    # not as strong but faster and used often,
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.SHA1PasswordHasher',
    'django.contrib.auth.hashers.CryptPasswordHasher',
)

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/ 
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

MEDIA_URL = '/media/'
MEDIA_ROOT = 'media'
STATIC_ROOT = ''
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
    os.path.join(BASE_DIR, "image_manipulation", "static"),
)

#Template folder locations
TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, "login", "templates"),
    os.path.join(BASE_DIR, "image_manipulation", "templates"),
    os.path.join(BASE_DIR, "templates"),
)

# allows template loading from main folder and app folders
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
if DEBUG:
   EMAIL_HOST = 'localhost'
   EMAIL_PORT = '1025'
   EMAIL_USE_TLS = False
   DEFAULT_FROM_EMAIL = 'testing@example.com'
   EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

#for sessions
SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'
SESSION_COOKIE_HTTPONLY = True # deny js access
SESSION_COOKIE_AGE = 31536000
