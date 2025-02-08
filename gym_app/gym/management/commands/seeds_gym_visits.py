from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User
from gym.models import GymVisit

# Create sample users if they don't already exist
alice, created = User.objects.get_or_create(username="alice")
bob, created = User.objects.get_or_create(username="bob")
charlie, created = User.objects.get_or_create(username="charlie")

# Get the current time
now = timezone.now()

# --- Sample Data for the Current Week and Month ---

# For testing, we want some visits to fall within this week's Sunday-Saturday range
# and some that are earlier in the month.
#
# NOTE: Adjust the days below to ensure the visits fall into the current week/month.
#
# For example, if today is Wednesday, make sure one of the dates is before Sunday of the current week.

# Visits for Alice
GymVisit.objects.create(
    user=alice,
    entry_time=now - timedelta(days=now.weekday()+2),  # e.g., last Sunday (adjust as needed)
    exit_time=now - timedelta(days=now.weekday()+2) + timedelta(hours=1),
    gym_location="Tepper"
)
GymVisit.objects.create(
    user=alice,
    entry_time=now - timedelta(days=1),  # yesterday; should be within current week
    exit_time=now - timedelta(days=1) + timedelta(hours=1),
    gym_location="Tepper"
)
# A visit earlier in the month but outside this week
GymVisit.objects.create(
    user=alice,
    entry_time=now - timedelta(days=10),
    exit_time=now - timedelta(days=10) + timedelta(hours=1),
    gym_location="Cohon"
)

# Visits for Bob
GymVisit.objects.create(
    user=bob,
    entry_time=now - timedelta(days=now.weekday()+1),  # e.g., this past Sunday
    exit_time=now - timedelta(days=now.weekday()+1) + timedelta(hours=1),
    gym_location="Tepper"
)
GymVisit.objects.create(
    user=bob,
    entry_time=now - timedelta(days=2),
    exit_time=now - timedelta(days=2) + timedelta(hours=1),
    gym_location="Cohon"
)
# A visit earlier in the month
GymVisit.objects.create(
    user=bob,
    entry_time=now - timedelta(days=15),
    exit_time=now - timedelta(days=15) + timedelta(hours=1),
    gym_location="Cohon"
)

# Visits for Charlie
GymVisit.objects.create(
    user=charlie,
    entry_time=now - timedelta(days=3),
    exit_time=now - timedelta(days=3) + timedelta(hours=1),
    gym_location="Tepper"
)
# A visit earlier in the month
GymVisit.objects.create(
    user=charlie,
    entry_time=now - timedelta(days=20),
    exit_time=now - timedelta(days=20) + timedelta(hours=1),
    gym_location="Cohon"
)

print("Sample gym visit data created successfully!")