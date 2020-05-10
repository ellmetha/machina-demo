"""
    Production Django settings
    ==========================

    This file imports the ``base`` settings and can add or modify previously defined settings to
    alter the configuration of the application for production environments.

    For more information on this file, see https://docs.djangoproject.com/en/dev/topics/settings/
    For the full list of settings and their values, see
    https://docs.djangoproject.com/en/dev/ref/settings/

"""

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from .base import *  # noqa: F403


# SENTRY CONFIGURATION
# ------------------------------------------------------------------------------

sentry_sdk.init(
    dsn=get_envsetting('SENTRY_DSN'),  # noqa: F405
    integrations=[DjangoIntegration()],
    environment='Production'
)
