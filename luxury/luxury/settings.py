from pathlib import Path
from django.contrib.messages import constants as messages
from huey import SqliteHuey

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-g33(tlrn-e+^78yorw$54kl%88u9h1r=^gv2548r7y+#6_0#ar"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']


# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "django.contrib.sites",
    "django.contrib.sitemaps",
    "rest_framework",
    "django_filters",
    "crispy_forms",
    "sorl.thumbnail",
    "ckeditor",
    "huey.contrib.djhuey",
    "users",
    "campaigns",
    "home",
    "categories",
    "products",
    "cart",
    "orders",
    "promo",
    "gallery",
    "integrations",
    "misc",
]

SITE_ID = 1

CRISPY_TEMPLATE_PACK = "bootstrap4"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

LOGIN_URL = "/user/cms/login/"

ROOT_URLCONF = "luxury.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "home.context_processors.main_settings",
                "categories.context_processors.main_categories",
                "cart.context_processors.cart_counter",
                "users.context_processors.wishlist_counter",
                "integrations.context_processors.integration",
            ],
        },
    },
]

WSGI_APPLICATION = "luxury.wsgi.application"

AUTH_USER_MODEL = "users.User"


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'luxury_p',
        'USER': 'luxury_p_db',
        'PASSWORD': '9Y2poMnd$0hy',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'sql_mode': 'traditional',
        }
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Kolkata"

USE_I18N = True

USE_L10N = False

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = '/home/xt6ylvsf4r6z/public_html/static/'
# STATICFILES_DIRS = [BASE_DIR / 'static']

MESSAGE_TAGS = {
    messages.ERROR: 'danger',
}

MEDIA_URL = '/media/'
MEDIA_ROOT = '/home/xt6ylvsf4r6z/public_html/media/'

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "bom1plmcpnl496198.prod.bom1.secureserver.net"
EMAIL_USE_SSL = True
EMAIL_PORT = 465
EMAIL_HOST_USER = "no-reply@theluxurypioneer.com"
EMAIL_HOST_PASSWORD = "no-reply@2023"
DEFAULT_FROM_EMAIL = "no-reply@theluxurypioneer.com"

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Huey
HUEY = SqliteHuey(filename=BASE_DIR / "tasks_db.sqlite3")

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https') 
