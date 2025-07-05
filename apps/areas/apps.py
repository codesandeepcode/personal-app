"""
Areas application configuration for Django.
This module defines the configuration for the Areas application within a Django project.
It sets the default auto field type and specifies the name of the application."""
from django.apps import AppConfig


class AreasConfig(AppConfig):
    """Areas application configuration class."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.areas'
