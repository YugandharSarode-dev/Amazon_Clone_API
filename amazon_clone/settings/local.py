from ..base import *

SECRET_KEY = "f#^st#9-kvv&c3pilne=tjv1$-vauyl@q3$$-yzkn6y0x3jdg#"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

# Database settings for app
DATABASES = {
    "default": {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'amazon_clone_db',        
        'USER': 'amazon_user',        
        'PASSWORD': 'reset123',
        'HOST': 'localhost',           
        'PORT': '5432',                
    }
}
CLIENT_ID = "P4Q4ZFCTLn6tBgC0byExMuiETHce5PIKkZEGjGxD"
CLIENT_SECRET = "5RjNUpkuFeo5QKKdBu6YcahgiRhTPNu3vOAUI693aoILX7tvZXEDLPd9DkaKIjPuKFE3gyQsPAXsd8Tfqkrjbdp9Phi0QMkYPpgzercJYQsXx1nnBJZpWvyjhjyzIHUy"

SERVER_PROTOCOLS = "http://"

ADMIN_EMAIL = "stark.official123@gmail.com"
FROM_EMAIL = "smtp@starkdigital.net"
EMAIL_HOST = "smtpout.secureserver.net"
EMAIL_HOST_USER = "smtp@starkdigital.net"
EMAIL_HOST_PASSWORD = "admin?963"
EMAIL_PORT = "465"
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_USE_SSL = True
EMAIL_USE_TLS = False
CC = []
S_KEY = b"ImmOpwdpqo5ALKyjzTOKkJeHihu0i9U4qN3XP2yx_jg="

FRONT_END_URL = "http://127.0.0.1:8000/"
BASE_URL = "http://0.0.0.0:8000/api/v1/"


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR + "/media/"
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        },
        "console": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "console",
        },
        "default": {
            "level": "WARNING",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "error.log",
            "maxBytes": 1024 * 1024 * 15,  # 15 MB
            "backupCount": 5,
            "formatter": "standard",
        },
        "request_handler": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "access.log",
            "maxBytes": 1024 * 1024 * 15,  # 15 MB
            "backupCount": 5,
            "formatter": "standard",
        },
    },
    "root": {
        "handlers": ["console", "default"],
        "level": "WARNING",
    },
    "loggers": {
        "django.db.backends": {
            "handlers": ["request_handler"],
            "level": "DEBUG",
        },
        "pymongo": {
            "handlers": ["default"],
            "level": "ERROR",
            "propagate": False,
        },
        "pymongo.topology": {
            "handlers": ["default"],
            "level": "ERROR",
            "propagate": False,
        },
        "pymongo.connection": {
            "handlers": ["default"],
            "level": "ERROR",
            "propagate": False,
        },
        "pymongo.command": {
            "handlers": ["default"],
            "level": "ERROR",
            "propagate": False,
        },
        "botocore": {
            "handlers": [],
            "level": "WARNING",
            "propagate": False,
        },
        "boto3": {
            "handlers": [],
            "level": "WARNING",
            "propagate": False,
        },
        "urllib3": {
            "handlers": [],
            "level": "WARNING",
            "propagate": False,
        },
        "celery": {
            "handlers": [],
            "level": "WARNING",
            "propagate": False,
        },
        "celery.utils.functional": {
            "handlers": [],
            "level": "WARNING",
            "propagate": False,
        },
        "instapermit": {
            "handlers": ["default"],
            "level": "INFO",
            "propagate": True,
        },
        "utility": {
            "handlers": ["default"],
            "level": "INFO",
            "propagate": True,
        },
        "sqs": {
            "handlers": [],
            "level": "WARNING",
            "propagate": False,
        },
    },
}

