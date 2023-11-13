"""
Django settings for projectile project.

Generated by 'django-admin startproject' using Django 4.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
from datetime import timedelta

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# The root of the git repo - Could be ~/project or ~/repo
REPO_DIR = os.path.realpath(os.path.join(BASE_DIR, ".."))
# The directory of the current user ie /home/django a.k.a. ~
HOME_DIR = os.path.realpath(os.path.join(REPO_DIR, ".."))
# The directory where collectstatic command copies/symlinks the files to
# This can/should be located at ~/staticfiles, preferrably outside the git repo
STATIC_DIR = os.path.realpath(os.path.join(HOME_DIR, "staticfiles"))
# The directory where different applications uploads media files to
# This can/should be located at ~/media, preferrably outside the git repo
MEDIA_DIR = os.path.realpath(os.path.join(HOME_DIR, "media"))

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_ROOT = STATIC_DIR
STATIC_URL = "/static/"

MEDIA_ROOT = MEDIA_DIR
MEDIA_URL = "/media/"


STATICFILES_DIRS = [os.path.join(REPO_DIR, "assets")]

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-l6^e&&#in^=$^93b0s7x4)eot3#dv22*(*5p^$^-q5o9canltx'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
PROJECT_APPS = [
    "catalogio",
    "core",
]

THIRD_PARTY_APPS = [
    "drf_yasg",
    "rest_framework",
    "social_django",
    "versatileimagefield",
    "rest_framework_simplejwt",
    "corsheaders",
    "django_filters",
]
INSTALLED_APPS = DJANGO_APPS + PROJECT_APPS + THIRD_PARTY_APPS

# swagger settings
SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {"basic": {"type": "basic"}},
}

REDOC_SETTINGS = {
    "LAZY_RENDERING": False,
}

AUTH_USER_MODEL = "core.User"

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'projectile.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        "DIRS": [os.path.join(BASE_DIR, "templates")],
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

WSGI_APPLICATION = 'projectile.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True



REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",

    ),
    # "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {"anon": "60/minute", "user": "120/minute"},
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 40,
}


AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'social_core.backends.google.GoogleOAuth2',
]

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "UPDATE_LAST_LOGIN": True,
}

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://aitools-staging.vercel.app"
]

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)
# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field


SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '654201802529-h3l30nfnnjr5oahptsjcq6j7oume7fbn.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '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'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


APPEND_SLASH = False

CORS_ALLOW_HEADERS = (
    "accept",
    "authorization",
    "content-type",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
    "x-domain",
    "userid",
)

'''

https://aitools-staging.vercel.app/

if os.environ.get("ENABLE_CORS_HEADERS", False) == "True":
    INSTALLED_APPS = [
        "corsheaders",
    ] + INSTALLED_APPS
    MIDDLEWARE = [
        "corsheaders.middleware.CorsMiddleware",
    ] + MIDDLEWARE

    CORS_ALLOW_CREDENTIALS = True
    CORS_ALLOWED_ORIGINS = [
        "http://localhost:3000",
        "http://localhost:4000",
        "http://127.0.0.1:5173",
        "https://aitools-staging.vercel.app",
    ]
    CSRF_TRUSTED_ORIGINS = [
        "http://localhost:3000",
        "http://localhost:4000",
        "http://127.0.0.1:5173",
        "https://aitools-staging.vercel.app",
    ]
    CORS_ALLOW_HEADERS = (
        *default_headers,
        "accept",
        "authorization",
        "content-type",
        "user-agent",
        "x-csrftoken",
        "x-requested-with",
        "x-domain",
    )
    CORS_ALLOWED_ORIGIN_REGEXES = [
        r"^http://\w+\.localhost:3000",
    ]
    CORS_ALLOW_ALL_ORIGINS = True

'''
