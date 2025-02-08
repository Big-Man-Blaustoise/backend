# gym/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer  # Optional, for explicit JSON rendering
from .models import GymVisit
from .serializers import GymVisitSerializer
from django.http import HttpResponse
from django.http import JsonResponse
from .utils import calculate_average_rating, get_time_based_ratings

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib import messages

from django.contrib.auth.models import User
from django.utils.dateparse import parse_datetime
from datetime import datetime


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
    
#these are for hourly average and daily average
def average_rating_view(request):
    """
    View that returns the average rating over the last hour.
    """
    avg_rating = calculate_average_rating()
    return JsonResponse({'average_rating': avg_rating})

def time_based_chart_view(request):
    """
    View that returns a time series of gym busyness ratings for the last 24 hours.
    """
    time_series = get_time_based_ratings()
    return JsonResponse({'time_series': time_series})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your account has been created! You can now log in.')
            return redirect('login')  # Redirect to login after registration
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})


#gym_visits per user
def get_user_gym_visits(request, user_id):
    """
    Get all gym visits for a specific user within a given date range.
    Expects query parameters: start_date, end_date (YYYY-MM-DD format)
    Example: /api/gym-visits/user/1/?start_date=2025-02-01&end_date=2025-02-07
    """
    try:
        user = User.objects.get(id=user_id)  # Get the user object

        # Get the query parameters
        start_date_str = request.GET.get('start_date')
        end_date_str = request.GET.get('end_date')

        # If we got the dates, parse them to datetime objects
        if start_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            start_time = datetime.combine(start_date, datetime.min.time())  # Set to 00:00:00
        else:
            start_time = None

        if end_date_str:
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
            end_time = datetime.combine(end_date, datetime.max.time())  # Set to 23:59:59
        else:
            end_time = None

        # Filter gym visits for the user in the date range
        gym_visits = GymVisit.objects.filter(user=user)

        if start_time:
            gym_visits = gym_visits.filter(entry_time__gte=start_time)
        if end_time:
            gym_visits = gym_visits.filter(entry_time__lte=end_time)

        # Prepare the response data
        visits_data = [
            {
                'entry_time': visit.entry_time.isoformat(),
                'gym_location': visit.gym_location,
                'gym_busy_rating': visit.gym_busy_rating,
            }
            for visit in gym_visits
        ]

        return JsonResponse({'user': user.username, 'gym_visits': visits_data}, safe=False)

    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
