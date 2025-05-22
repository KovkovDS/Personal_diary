from django.core.management.base import BaseCommand
from django.core.management import call_command
from personal_diary.models import DiaryEntry


class Command(BaseCommand):
    help = 'Load test data for groups from fixture'

    def handle(self, *args, **kwargs):
        DiaryEntry.objects.all().delete()

        call_command('loaddata', 'diary_entries_fixture.json')
        self.stdout.write(self.style.SUCCESS('Successfully loaded data from fixture'))
