import os

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Load all fixture files"

    def handle(self, *args, **options):
        apps = settings.INSTALLED_APPS

        for app in apps:
            fixture_dir = os.path.join(settings.BASE_DIR, app, 'fixtures')

            if os.path.exists(fixture_dir):
                for filename in os.listdir(fixture_dir):
                    if filename.endswith('.json'):
                        fixture_file = os.path.join(fixture_dir, filename)
                        self.stdout.write(self.style.SUCCESS(f'Loading fixture {fixture_file}'))
                        call_command('loaddata', fixture_file)

        self.stdout.write(self.style.SUCCESS('Successfully loaded all fixtures'))
