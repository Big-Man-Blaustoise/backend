import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from gym.models import GymVisit
from faker import Faker

class Command(BaseCommand):
    help = 'Populate the GymVisit model with fake data'

    def handle(self, *args, **kwargs):
        fake = Faker()
        
        # Create 5 sample users (adjust the number if needed)
        users = []
        for _ in range(5):  # Creating 5 sample users
            user = User.objects.create_user(
                username=fake.user_name(),
                password=fake.password(),
                email=fake.email()
            )
            users.append(user)
        
        # Generate GymVisit data for each user
        for user in users:
            for _ in range(10):  # 10 visits per user
                entry_time = fake.date_time_this_year(before_now=True, after_now=False)
                gym_location = random.choice(['Cohon', 'Tepper'])  # Random gym location
                gym_busy_rating = random.randint(0, 4)  # Random rating from 0 to 4
                
                # Create a GymVisit object
                GymVisit.objects.create(
                    user=user,
                    entry_time=entry_time,
                    gym_location=gym_location,
                    gym_busy_rating=gym_busy_rating
                )
        
        self.stdout.write(self.style.SUCCESS('Successfully populated GymVisit data with fake data'))
