# gym/utils.py
from datetime import timedelta
from django.utils import timezone
from .models import GymVisit

def calculate_average_rating():
    """
    Calculate the average gym rating over the last hour (or custom time range).
    """
    one_hour_ago = timezone.now() - timedelta(hours=1)
    recent_visits = GymVisit.objects.filter(entry_time__gte=one_hour_ago)
    
    # Assuming you store the 'gym_busyness' as an integer in the model (e.g., 0, 1, 2, 3)
    if recent_visits.exists():
        total_rating = sum(visit.gym_busy_rating for visit in recent_visits)
        average_rating = total_rating / len(recent_visits)
    else:
        average_rating = 0  # Default to 0 if no visits in the last hour

    return average_rating

def get_time_based_ratings():
    """
    Get a time-based series of gym busyness over the last 24 hours.
    Returns a list of tuples with (time, rating).
    """
    time_series = []
    now = timezone.now()
    one_day_ago = now - timedelta(days=1)
    
    # We will create 24 hourly bins
    for i in range(24):
        time_bin_start = now - timedelta(hours=i)
        time_bin_end = now - timedelta(hours=(i-1))

        # Get average rating for this hour (if available)
        visits_in_bin = GymVisit.objects.filter(entry_time__gte=time_bin_start, entry_time__lt=time_bin_end)
        
        if visits_in_bin.exists():
            # Sum up the gym_busy_rating values and calculate the average
            avg_rating_in_bin = sum(visit.gym_busy_rating for visit in visits_in_bin) / len(visits_in_bin)
        else:
            avg_rating_in_bin = 0

        time_series.append({
            'time': time_bin_start.strftime('%H:%M'),
            'avg_rating': avg_rating_in_bin
        })
    
    return time_series
