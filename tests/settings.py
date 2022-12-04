import os

DEBUG = True

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = "django-treenode"

ALLOWED_HOSTS = ["*"]

database_engine = os.environ.get("DATABASE_ENGINE", "sqlite")
database_config = {
    "sqlite": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    },
    # 'mysql': {
    #     'ENGINE': 'django.db.backends.mysql',
    #     'NAME': 'treenode',
    #     'USER': 'mysql',
    #     'PASSWORD': 'mysql',
    #     'HOST': '',
    #     'PORT': '',
    # },
    "postgres": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "treenode",
        "USER": "postgres",
        "PASSWORD": "postgres",
        "HOST": "",
        "PORT": "",
    },
}

github_workflow = os.environ.get("GITHUB_WORKFLOW")
if github_workflow:
    database_config["postgres"]["NAME"] = "postgres"
    database_config["postgres"]["HOST"] = "127.0.0.1"
    database_config["postgres"]["PORT"] = "5432"

DATABASES = {
    "default": database_config.get(database_engine),
}

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "django.contrib.sessions",
    "tests",
    "treenode",
]

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

MIDDLEWARE = [
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.request",
                "django.contrib.messages.context_processors.messages",
            ],
            "debug": DEBUG,
        },
    },
]

MEDIA_ROOT = os.path.join(BASE_DIR, "treenode/public/media/")
MEDIA_URL = "/media/"

STATIC_ROOT = os.path.join(BASE_DIR, "treenode/public/static/")
STATIC_URL = "/static/"
