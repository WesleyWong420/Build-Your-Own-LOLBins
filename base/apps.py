"""
WESLEY WONG KEE HAN
TP059618 APU3F2205CS(CYB)

Applications for BYOL
"""

from django.apps import AppConfig
from django.conf import settings
import subprocess

class BaseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'base'

    def ready(self):
        subprocess.Popen(["python", "-m", "http.server", "8000", "-d", settings.MEDIA_ROOT])
        return True