import os
import re
from pathlib import Path
import environ
# import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False),
    ENVIRONMENT=(str, "development"),
    SECRET_KEY=(str, "django-insecure-dummy-key-for-builds-and-dev-only"),
    # DATABASE_URL=(str, "sqlite:///dummy.db"),
    ALLOWED_HOSTS=(str, "*"),
    CSRF_TRUSTED_ORIGINS=(str, "https://*, http://*"),
    USE_X_FORWARDED_HOST=(bool, False),
    WAGTAIL_SITE_NAME=(str, "Wagtail Starter Kit"),
    WAGTAILADMIN_BASE_URL=(str, "http://localhost:8000"),
)

# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG")


INSTALLED_APPS = [
    # Django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Wagtail apps
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.search",
    "wagtail.admin",
    "wagtail",
    # Optional Wagtail apps
    "wagtail.contrib.routable_page",
    "wagtail.contrib.settings",
    "wagtail.contrib.search_promotions",
    # Third-party apps
    "taggit",
    "modelcluster",
    # SEO
    "wagtailseo",
    # Caching
    "wagtailcache",
    # Forms
    "wagtail_flexible_forms",
    # Frontend integration
    "django_vite",
    "turbo_helper",
    # Our apps
    "apps.core",
    "apps.pages",
    "apps.blocks",
    "apps.navigation.apps.NavigationConfig",
    "apps.settings",
    "apps.search",
    "apps.forms",
    "apps.snippets",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
    "turbo_helper.middleware.TurboMiddleware",
]

if not DEBUG:
    MIDDLEWARE.insert(1, "wagtailcache.cache.UpdateCacheMiddleware")
    MIDDLEWARE.append("wagtailcache.cache.FetchFromCacheMiddleware")

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "wagtail.contrib.settings.context_processors.settings",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

# DATABASES = {
#     "default": dj_database_url.config(
#         default=env("DATABASE_URL"),
#         conn_max_age=600,
#         conn_health_checks=True,
#     )
# }

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db/database.db",
        "OPTIONS": {
            "transaction_mode": "IMMEDIATE",
            "timeout": 5,  # seconds
            "init_command": """
                PRAGMA journal_mode=WAL;
                PRAGMA synchronous=NORMAL;
                PRAGMA mmap_size=134217728;
                PRAGMA journal_size_limit=27103364;
                PRAGMA cache_size=2000;
            """,
        },
    },
    "cache": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db/cache.db",
        "OPTIONS": {
            "transaction_mode": "IMMEDIATE",
            "timeout": 5,  # seconds
            "init_command": """
                PRAGMA journal_mode=WAL;
                PRAGMA synchronous=NORMAL;
                PRAGMA mmap_size=134217728;
                PRAGMA journal_size_limit=27103364;
                PRAGMA cache_size=2000;
            """,
        },
    },
}

DATABASE_ROUTERS = ["config.routers.CacheRouter"]


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATICFILES_DIRS = [
    BASE_DIR / "frontend/dist",  # Vite build output
]

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATIC_URL = "/static/"

# S3 settings for media files (used by default)
STORAGES = {
    "default": {
        "BACKEND": "config.storage.CustomS3Boto3Storage",
        "OPTIONS": {
            "public_endpoint_url": env(
                "AWS_S3_PUBLIC_ENDPOINT_URL", default="http://localhost:9000"
            ),
        },
    },
    "staticfiles": {
        # "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

# AWS settings for S3
AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME")
AWS_S3_REGION_NAME = env("AWS_S3_REGION_NAME", default="us-east-1")
AWS_S3_ENDPOINT_URL = env("AWS_S3_ENDPOINT_URL", default=None)
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
AWS_S3_VERIFY = True
AWS_QUERYSTRING_AUTH = True

# When using MinIO, we need to set this to False to avoid SSL issues
AWS_S3_SECURE_URLS = env("AWS_S3_SECURE_URLS", default=True)

# Ensure query string authentication is enabled and set expiration
AWS_QUERYSTRING_EXPIRE = env(
    "AWS_QUERYSTRING_EXPIRE", default=1800
)  # 1/2 hour expiration


# http://whitenoise.evans.io/en/stable/django.html#WHITENOISE_IMMUTABLE_FILE_TEST
def immutable_file_test(path, url):
    # Match vite (rollup)-generated hashes, à la, `some_file-CSliV9zW.js`
    return re.match(r"^.+[.-][0-9a-zA-Z_-]{8,12}\..+$", url)


WHITENOISE_IMMUTABLE_FILE_TEST = immutable_file_test

# Django-Vite Settings
# ------------------------------------------------------------------------------
DJANGO_VITE = {
    "default": {
        "dev_mode": True if env("ENVIRONMENT") == "development" else False,
        "dev_server_host": "localhost",
        "dev_server_port": 5173,
    }
}


MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Wagtail settings
WAGTAIL_SITE_NAME = env("WAGTAIL_SITE_NAME")
WAGTAILADMIN_BASE_URL = env("WAGTAILADMIN_BASE_URL")

# Disable password validators for development
AUTH_PASSWORD_VALIDATORS = []

# SECURITY WARNING: define the correct hosts in production!
# This should be set to your domain or IP address in production
ALLOWED_HOSTS = env("ALLOWED_HOSTS").split(",")
CSRF_TRUSTED_ORIGINS = env("CSRF_TRUSTED_ORIGINS").split(",")
USE_X_FORWARDED_HOST = env("USE_X_FORWARDED_HOST")

# Increase the maximum number of fields for complex page models
DATA_UPLOAD_MAX_NUMBER_FIELDS = 10000

# Wagtail Cache settings
WAGTAIL_CACHE = True
WAGTAIL_CACHE_BACKEND = "default"

# Cache settings
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.db.DatabaseCache",
        "LOCATION": "cache",
    }
}

# Webpack loader settings
WEBPACK_LOADER = {
    "MANIFEST_FILE": os.path.join(BASE_DIR, "apps/frontend/build/manifest.json"),
}
