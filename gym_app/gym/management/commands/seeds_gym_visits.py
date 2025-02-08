from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from gym.models import GymVisit

class Command(BaseCommand):
    help = 'Seeds the database with sample gym visit data for testing'

    def handle(self, *args, **kwargs):
        # Get current time
        now = timezone.now()

        # -- User "alice" --
        # Visits within the last 7 days (week)
        GymVisit.objects.create(
            user="alice", 
            entry_time=now - timedelta(days=2), 
            exit_time=now - timedelta(days=2) + timedelta(hours=1), 
            gym_location="Tepper"
        )
        GymVisit.objects.create(
            user="alice", 
            entry_time=now - timedelta(days=1), 
            exit_time=now - timedelta(days=1) + timedelta(hours=1), 
            gym_location="Tepper"
        )
        GymVisit.objects.create(
            user="alice", 
            entry_time=now - timedelta(days=6), 
            exit_time=now - timedelta(days=6) + timedelta(hours=1), 
            gym_location="Cohon"
        )
        # Visits older than 7 days but within 30 days (month)
        GymVisit.objects.create(
            user="alice", 
            entry_time=now - timedelta(days=10), 
            exit_time=now - timedelta(days=10) + timedelta(hours=1), 
            gym_location="Cohon"
        )
        GymVisit.objects.create(
            user="alice", 
            entry_time=now - timedelta(days=15), 
            exit_time=now - timedelta(days=15) + timedelta(hours=1), 
            gym_location="Tepper"
        )

        # -- User "bob" --
        # Visits within the last 7 days (week)
        GymVisit.objects.create(
            user="bob", 
            entry_time=now - timedelta(days=3), 
            exit_time=now - timedelta(days=3) + timedelta(hours=1), 
            gym_location="Tepper"
        )
        GymVisit.objects.create(
            user="bob", 
            entry_time=now - timedelta(days=5), 
            exit_time=now - timedelta(days=5) + timedelta(hours=1), 
            gym_location="Cohon"
        )
        # Visits older than 7 days but within 30 days (month)
        GymVisit.objects.create(
            user="bob", 
            entry_time=now - timedelta(days=8), 
            exit_time=now - timedelta(days=8) + timedelta(hours=1), 
            gym_location="Cohon"
        )
        GymVisit.objects.create(
            user="bob", 
            entry_time=now - timedelta(days=20), 
            exit_time=now - timedelta(days=20) + timedelta(hours=1), 
            gym_location="Tepper"
        )

        # -- User "charlie" --
        # Visit within the last 7 days (week)
        GymVisit.objects.create(
            user="charlie", 
            entry_time=now - timedelta(days=4), 
            exit_time=now - timedelta(days=4) + timedelta(hours=1), 
            gym_location="Tepper"
        )
        # Visit older than 7 days but within 30 days (month)
        GymVisit.objects.create(
            user="charlie", 
            entry_time=now - timedelta(days=25), 
            exit_time=now - timedelta(days=25) + timedelta(hours=1), 
            gym_location="Cohon"
        )

        self.stdout.write(self.style.SUCCESS('Sample gym visit data created successfully!'))