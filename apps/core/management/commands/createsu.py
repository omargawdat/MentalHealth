from django.core.management.base import BaseCommand

from apps.authentication.models import CustomUser


class Command(BaseCommand):
    def handle(self, *args, **options):
        admin_email = "admin@example.com"
        admin_password = "123"
        if not CustomUser.objects.filter(email=admin_email).exists():
            CustomUser.objects.create_superuser(
                email=admin_email,
                password=admin_password,
            )
            self.stdout.write(self.style.SUCCESS('Successfully created new super user'))
