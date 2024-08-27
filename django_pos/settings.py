import os
from pathlib import Path

# To keep secret keys in environment variables
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY", False)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DEBUG", False)

ALLOWED_HOSTS = ["*"]


# =================================== APPLICATION DEFINITION ===================================
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "social_django",
    # =================================== OTHER APPLICATIONS ===================================
    "bootstrap5",
    "formtools",
    "crispy_forms",
    "crispy_bootstrap5",
    "django.contrib.humanize",
    # =================================== PROJECT APPLICATIONS ===================================
    "apps.authentication",
]

MIDDLEWARE = [
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "social_django.middleware.SocialAuthExceptionMiddleware",
]

ROOT_URLCONF = "django_pos.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR, "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "social_django.context_processors.backends",
                "social_django.context_processors.login_redirect",
                # Other context processors
                "apps.authentication.context_processors.guest_profiles_context",
                "apps.authentication.context_processors.guest_user_feedback_context",
            ],
        },
    },
]

WSGI_APPLICATION = "django_pos.wsgi.application"


# =================================== DATABASE CONFIGURATIONS ===================================
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME", "default_db_name"),
        "USER": os.environ.get("DB_USER", "default_user"),
        "PASSWORD": os.environ.get("DB_PASSWORD", "default_password"),
        "HOST": os.environ.get("DB_HOST", "localhost"),
        "PORT": os.environ.get("DB_PORT", "5432"),
    }
}


# =================================== PASSWORD VALIDATION ===================================
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

# A tuple of authentication backends that Django will use for authentication.
AUTHENTICATION_BACKENDS = (
    "social_core.backends.github.GithubOAuth2",
    "social_core.backends.google.GoogleOAuth2",
    # 'social_core.backends.twitter.TwitterOAuth',
    # "social_core.backends.linkedin.LinkedinOAuth2",
    "django.contrib.auth.backends.ModelBackend",
)


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files like CSS, JavaScript, or images will be served under the `/static/` URL path.
# https://docs.djangoproject.com/en/3.2/howto/static-files/
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static/"]


# `MEDIA_ROOT` and `MEDIA_URL` are settings in a Django project related to handling media files such
# as user-uploaded images, files, etc.
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"


# The `LOGIN_REDIRECT_URL` setting in Django specifies the URL where the user will be redirected to
# after a successful login. In this case, it is set to `"/"` which means that after a user
# successfully logs in, they will be redirected to the root URL of the website.
LOGIN_REDIRECT_URL = "/"
LOGIN_URL = "login"

# =================================== SOCIIAL AUTH CONFIGURATIONS ===================================
# social auth configs for github
SOCIAL_AUTH_GITHUB_KEY = str(os.getenv("GITHUB_KEY"))
SOCIAL_AUTH_GITHUB_SECRET = str(os.getenv("GITHUB_SECRET"))

# social auth configs for google
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = str(os.getenv("GOOGLE_KEY"))
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = str(os.getenv("GOOGLE_SECRET"))


# =================================== EMAIL CONFIGURATIONS ===================================
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = str(os.getenv("EMAIL_USER"))
EMAIL_HOST_PASSWORD = str(os.getenv("EMAIL_PASS"))

SESSION_COOKIE_AGE = 3600  # 60 * 60 Session duration in seconds
SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # Expire session when browser closes

# Specifying default primary key field type for models that don't define a primary key field explicitly.
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# =================================== SETTINGS TO DJANGO CRISPY FORMS PACKAGE ===================================
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"


# =================================== USE THE LOGGER ===================================
LOGS_DIR = BASE_DIR / "logs"
LOGS_DIR.mkdir(
    parents=True, exist_ok=True
)  # Create a 'logs' directory inside your project folder if it doesn't exist

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
        },
        "file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": LOGS_DIR / "app.log",  # Path to your log file
        },
    },
    "loggers": {
        "": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
}
