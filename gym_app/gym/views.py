# gym/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer  # Optional, for explicit JSON rendering
from .models import GymVisit
from .serializers import GymVisitSerializer, ProfileSerializer
from django.http import HttpResponse, JsonResponse
from django.db.models import Count
from django.utils import timezone
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import timedelta, datetime, time
from django.utils.timezone import make_aware
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from gym.models import Profile 



def home(request):
    return HttpResponse("Welcome to the Gym App!")

class GymVisitList(APIView):
    # Optional: If you want to explicitly specify that the response should be in JSON format
    renderer_classes = [JSONRenderer]

    def get(self, request):
        # Get all gym visit records
        visits = GymVisit.objects.all()
        # Serialize the data
        serializer = GymVisitSerializer(visits, many=True)
        # Return the data as a JSON response
        return Response(serializer.data)

def leaderboard(request):
    # Get today's local date
    today = timezone.localdate()

    # --- WEEKLY BOUNDARIES (Sunday to Saturday) ---
    # In Python, weekday() returns Monday=0, ... Sunday=6.
    # To get the most recent Sunday, calculate:
    days_since_sunday = (today.weekday() + 1) % 7  
    start_of_week = today - timedelta(days=days_since_sunday)
    end_of_week = start_of_week + timedelta(days=6)

    # Convert the date boundaries to timezone-aware datetimes
    start_of_week_dt = make_aware(datetime.combine(start_of_week, time.min))
    end_of_week_dt = make_aware(datetime.combine(end_of_week, time.max))

    # --- MONTHLY BOUNDARIES (Current Calendar Month) ---
    start_of_month = today.replace(day=1)
    start_of_month_dt = make_aware(datetime.combine(start_of_month, time.min))
    # For the monthly leaderboard, we consider all visits from the start of the month until now.
    
    # --- QUERYING THE DATABASE ---
    # Weekly leaderboard: visits between start_of_week_dt and end_of_week_dt.
    week_queryset = (
        GymVisit.objects.filter(entry_time__gte=start_of_week_dt, entry_time__lte=end_of_week_dt)
        .values('user__username')
        .annotate(visit_count=Count('id'))
        .order_by('-visit_count')
    )
    
    # Monthly leaderboard: visits since the first day of the month.
    month_queryset = (
        GymVisit.objects.filter(entry_time__gte=start_of_month_dt)
        .values('user__username')
        .annotate(visit_count=Count('id'))
        .order_by('-visit_count')
    )
    
    # --- BUILDING THE JSON RESPONSE WITH CLICKABLE PROFILE URLs ---
    week_leaderboard = []
    for entry in week_queryset:
        username = entry['user__username']
        profile = get_object_or_404(Profile, user__username=username)
        serializer = ProfileSerializer(profile)
        week_leaderboard.append({
            'user': username,
            'visit_count': entry['visit_count'],
            'profile': serializer.data,
        })
        
    month_leaderboard = []
    for entry in month_queryset:
        username = entry['user__username']
        profile = get_object_or_404(Profile, user__username=username)
        month_leaderboard.append({
            'user': username,
            'visit_count': entry['visit_count'],
            'profile': serializer.data,
        })
    
    data = {
        "week_leaderboard": week_leaderboard,
        "month_leaderboard": month_leaderboard
    }
    
    return JsonResponse(data)

def profile_detail(request, username):
    # Retrieve the user by username; assuming each user has an associated profile.
    user = get_object_or_404(User, username=username)
    # Render a template (e.g., 'profile_detail.html') and pass the user's profile
    return render(request, 'profile_detail.html', {'profile': user.profile})