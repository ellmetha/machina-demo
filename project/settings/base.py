"""
    Base Django settings for the machina-vanilla demo project
    =========================================================

    For more information on this file, see https://docs.djangoproject.com/en/dev/topics/settings/
    For the full list of settings and their values, see
    https://docs.djangoproject.com/en/dev/ref/settings/

"""

import json
import os
import pathlib

from django.core.exceptions import ImproperlyConfigured
from django.urls import reverse_lazy
from machina import MACHINA_MAIN_STATIC_DIR, MACHINA_MAIN_TEMPLATE_DIR


# BASE DIRECTORIES
# ------------------------------------------------------------------------------

# Two base directories are considered for this project:
# The PROJECT_PATH corresponds to the path towards the root of this project (the root of the
# repository).
# The INSTALL_PATH corresponds to the path towards the directory where the project's repository
# is present on the filesystem.
# By default INSTALL_PATH has the same than PROJECT_PATH.

PROJECT_PATH = pathlib.Path(__file__).parents[2]
INSTALL_PATH = pathlib.Path(os.environ.get('DJANGO_INSTALL_PATH')) \
    if 'DJANGO_INSTALL_PATH' in os.environ else PROJECT_PATH


# ENVIRONMENT SETTINGS HANDLING
# ------------------------------------------------------------------------------

ENVSETTINGS_FILENAME = '.env.json'
ENVSETTINGS_NIL = object()

# JSON-based environment module
with open(os.environ.get('ENVSETTINGS_FILEPATH') or str(INSTALL_PATH / ENVSETTINGS_FILENAME)) as f:
    secrets = json.loads(f.read())


def get_envsetting(setting, default=ENVSETTINGS_NIL, secrets=secrets):
    """ Get the environment setting variable or return explicit exception. """
    try:
        return secrets[setting]
    except KeyError:
        if default is not ENVSETTINGS_NIL:
            return default
        error_msg = 'Set the {0} environment variable in the {1} file'.format(
            setting, ENVSETTINGS_FILENAME)
        raise ImproperlyConfigured(error_msg)


# APP CONFIGURATION
# ------------------------------------------------------------------------------

INSTALLED_APPS = [
    # Django apps
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',

    # Third party apps
    'captcha',
    'haystack',
    'mptt',
    'widget_tweaks',

    # Machina apps:
    'machina',
    'machina.apps.forum',
    'machina.apps.forum_conversation',
    'machina.apps.forum_conversation.forum_attachments',
    'machina.apps.forum_conversation.forum_polls',
    'machina.apps.forum_feeds',
    'machina.apps.forum_moderation',
    'machina.apps.forum_search',
    'machina.apps.forum_tracking',
    'machina.apps.forum_member',
    'machina.apps.forum_permission',
]


# MIDDLEWARE CONFIGURATION
# ------------------------------------------------------------------------------

MIDDLEWARE = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.sites.middleware.CurrentSiteMiddleware',
    'machina.apps.forum_permission.middleware.ForumPermissionMiddleware',
)


# DEBUG CONFIGURATION
# ------------------------------------------------------------------------------

# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = False


# DATABASE CONFIGURATION
# ------------------------------------------------------------------------------

# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': get_envsetting('DB_ENGINE'),
        'NAME': get_envsetting('DB_NAME'),
        'USER': get_envsetting('DB_USER'),
        'PASSWORD': get_envsetting('DB_PASSWORD'),
        'HOST': get_envsetting('DB_HOST'),
        'OPTIONS': get_envsetting('DB_OPTIONS'),
    },
}


# GENERAL CONFIGURATION
# ------------------------------------------------------------------------------

# See: https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = 'en'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1

# See: https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = get_envsetting('ALLOWED_HOSTS')

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TIME_ZONE
TIME_ZONE = 'EST'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#languages
LANGUAGES = (
    ('en', 'English'),
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#locale-paths
LOCALE_PATHS = (
    str(PROJECT_PATH / 'project' / 'locale'),
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-ADMINS
ADMINS = (
    ('dev', get_envsetting('EMAIL_DEV')),
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-MANAGERS
MANAGERS = (
    ('team', get_envsetting('EMAIL_TEAM')),
)


# EMAIL CONFIGURATION
# ------------------------------------------------------------------------------

# See: https://docs.djangoproject.com/en/dev/ref/settings/#default-from-email
DEFAULT_FROM_EMAIL = get_envsetting('DEFAULT_FROM_EMAIL')

# See: https://docs.djangoproject.com/en/dev/ref/settings/#server-email
SERVER_EMAIL = get_envsetting('SERVER_EMAIL')

# See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-EMAIL_USE_TLS
EMAIL_USE_TLS = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-host
EMAIL_HOST = get_envsetting('EMAIL_HOST')

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-host-user
EMAIL_HOST_USER = get_envsetting('EMAIL_HOST_USER')

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-host-password
EMAIL_HOST_PASSWORD = get_envsetting('EMAIL_HOST_PASSWORD')

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-port
EMAIL_PORT = 587


# SECRET CONFIGURATION
# ------------------------------------------------------------------------------

# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = get_envsetting('SECRET_KEY')


# TEMPLATE CONFIGURATION
# ------------------------------------------------------------------------------

# See: https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': (
            str(PROJECT_PATH / 'main' / 'templates'),
            MACHINA_MAIN_TEMPLATE_DIR,
        ),
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
                'machina.core.context_processors.metadata',
            ],
            'loaders': [
                ('django.template.loaders.cached.Loader', (
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader',
                )),
            ]
        },
    },
]


# STATIC FILE CONFIGURATION
# ------------------------------------------------------------------------------

# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = str(INSTALL_PATH / 'static')

# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = '/static/'

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = (
    MACHINA_MAIN_STATIC_DIR,
    str(PROJECT_PATH / 'main' / 'static' / 'build'),
    str(PROJECT_PATH / 'main' / 'static'),
)

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-STATICFILES_STORAGE
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'


# MEDIA CONFIGURATION
# ------------------------------------------------------------------------------

# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = str(INSTALL_PATH / 'media')

# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = '/media/'


# URL CONFIGURATION
# ------------------------------------------------------------------------------

# See: https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF = 'project.urls'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = 'wsgi.application'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#login-url
LOGIN_URL = reverse_lazy('login')


# ADMIN CONFIGURATION
# ------------------------------------------------------------------------------

# URL of the admin page
ADMIN_URL = get_envsetting('ADMIN_URL')


# CACHE CONFIGURATION
# ------------------------------------------------------------------------------

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    },
    'machina_attachments': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/tmp',
    }
}


# RECAPTCHA CONFIGURATION
# ------------------------------------------------------------------------------

RECAPTCHA_PUBLIC_KEY = get_envsetting('RECAPTCHA_PUBLIC_KEY')
RECAPTCHA_PRIVATE_KEY = get_envsetting('RECAPTCHA_PRIVATE_KEY')
NOCAPTCHA = True


# HAYSTTACK CONFIGURATION
# ------------------------------------------------------------------------------

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': str(INSTALL_PATH / '.whoosh_index'),
    },
}


# MACHINA CONFIGURATION
# ------------------------------------------------------------------------------

MACHINA_DEFAULT_AUTHENTICATED_USER_FORUM_PERMISSIONS = [
    'can_see_forum',
    'can_read_forum',
    'can_start_new_topics',
    'can_reply_to_topics',
    'can_edit_own_posts',
    'can_post_without_approval',
    'can_create_polls',
    'can_vote_in_polls',
    'can_download_file',
]

MACHINA_PROFILE_AVATAR_WIDTH = 0
MACHINA_PROFILE_AVATAR_HEIGHT = 0
MACHINA_PROFILE_AVATAR_MIN_WIDTH = 60
MACHINA_PROFILE_AVATAR_MAX_WIDTH = 150
MACHINA_PROFILE_AVATAR_MIN_HEIGHT = 100
MACHINA_PROFILE_AVATAR_MAX_HEIGHT = 250
MACHINA_PROFILE_AVATAR_MAX_UPLOAD_SIZE = 300000
