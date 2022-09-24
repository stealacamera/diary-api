from django.core.management.base import BaseCommand
from datetime import datetime, timedelta

from diary.models import Entry


class Command(BaseCommand):
    help = 'Deletes entries in the trash after 30 days'
    
    def handle(self, *args, **options):
        Entry.objects.filter(deleted=True, edited_on=datetime.now() - timedelta(days=30)).delete()