# depression_detection_command.py

from django.core.management.base import BaseCommand
from apps.journal.scripts.Dep_test import predict as predict_depression
from apps.journal.models import JournalEntry

class Command(BaseCommand):
    help = 'Detect depression for journal entries'

    def handle(self, *args, **kwargs):
        entries = JournalEntry.objects.all()
        for entry in entries:
            depression_prediction = predict_depression(entry.notes)
            entry.has_depression = depression_prediction
            entry.save()
