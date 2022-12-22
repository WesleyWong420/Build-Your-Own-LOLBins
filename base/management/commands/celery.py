import sys
import shlex
import subprocess
from django.core.management.base import BaseCommand
from django.utils import autoreload

class Command(BaseCommand):
    def handle(self, *args, **options):
        autoreload.run_with_reloader(self._restart_celery)

    @classmethod
    def _restart_celery(cls):
        if sys.platform == "win32":
            cls.run('taskkill /f /t /im celery.exe')
            cls.run('celery -A BYOL purge -f')
            cls.run('celery -A BYOL worker -l info -P solo')

    @staticmethod
    def run(cmd):
        subprocess.call(shlex.split(cmd))