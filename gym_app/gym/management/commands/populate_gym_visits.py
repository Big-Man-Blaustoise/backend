# gym/management/commands/populate_gym_visits.py
from django.core.management.base import BaseCommand
from gym.models import GymVisit
from faker import Faker
import random
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Populate the GymVisit model with fake data'

    def handle(self, *args, **kwargs):
        fake = Faker()
        now = timezone.now()

        for _ in range(100):  # Adjust the number to generate as many records as you want
            user = fake.name()  # Generate a fake name for the user
            entry_time = fake.date_time_this_year(before_now=True, after_now=False)  # Entry time within this year
            #gym_location = fake.city()  # Random gym location (could be a city)
            gym_busy_rating = random.randint(0, 4)  # Random rating from 0 to 4
            
            # Create a GymVisit object
            GymVisit.objects.create(
                user=user,
                entry_time=entry_time,
                gym_location="Cohon",
                gym_busy_rating=gym_busy_rating
            )
            
        self.stdout.write(self.style.SUCCESS('Successfully populated GymVisit model with fake data.'))
