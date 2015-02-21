from settings import *

DEBUG = TEMPLATE_DEBUG = False
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'stitchpick',
        'USER': 'deployer',
        'PASSWORD': 'M93vba!x0',
        'HOST': 'localhost',
        'PORT': '',
    }
}
