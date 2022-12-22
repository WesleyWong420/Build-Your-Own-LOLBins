"""
WESLEY WONG KEE HAN
TP059618 APU3F2205CS(CYB)

Applications for BYOL
"""

from django.apps import AppConfig

class BaseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'base'

    def ready(self):
        return True