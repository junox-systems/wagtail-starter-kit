from .base import *  # noqa: F401, F403
from .base import env, environ, STORAGES, DATABASES

environ.Env.read_env("/usr/local/etc/wagtail/env")

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DJANGO_DEBUG")

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Django-Vite Settings
# ------------------------------------------------------------------------------
DJANGO_VITE = {
    "default": {
        "dev_mode": False,
    }
}

# Wagtail Cache settings
WAGTAIL_CACHE = True
WAGTAIL_CACHE_BACKEND = "default"
WAGTAIL_CACHE_KEYRING = True
WAGTAIL_CACHE_HEADER = "X-App-Cache"
WAGTAIL_CACHE_IGNORE_COOKIES = True

# Wagtail settings
WAGTAIL_SITE_NAME = env("WAGTAIL_SITE_NAME")
WAGTAILADMIN_BASE_URL = env("WAGTAILADMIN_BASE_URL")

# Cache settings
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "wsk-cache",
        "TIMEOUT": 60 * 60 * 24 * 7,  # 1 week
    }
}

AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID", default="minioadmin")
AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY", default="minioadmin")
AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME", default="bucket")
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

# SECURITY WARNING: define the correct hosts in production!
# This should be set to your domain or IP address in production
ALLOWED_HOSTS = env("ALLOWED_HOSTS").split(",")
CSRF_TRUSTED_ORIGINS = env("CSRF_TRUSTED_ORIGINS").split(",")
USE_X_FORWARDED_HOST = env("USE_X_FORWARDED_HOST")
USE_X_FORWARDED_PORT = env("USE_X_FORWARDED_PORT")

STORAGES["default"]["OPTIONS"]["public_endpoint_url"] = env(
    "AWS_S3_PUBLIC_ENDPOINT_URL", default="http://localhost:9000"
)

# Database Path
DATABASES["default"]["NAME"] = env("DATABASE_PATH")
