# stress_detection_command.py

from django.core.management.base import BaseCommand
from apps.journal.scripts.Stress_test import predict as predict_stress
from apps.journal.models import JournalEntry

class Command(BaseCommand):
    help = 'Detect stress for journal entries'

    def handle(self, *args, **kwargs):
        entries = JournalEntry.objects.all()
        for entry in entries:
            stress_prediction = predict_stress(entry.notes)
            entry.has_stress = stress_prediction
            entry.save()
