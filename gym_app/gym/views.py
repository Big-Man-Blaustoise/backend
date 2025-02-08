# gym/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer  # Optional, for explicit JSON rendering
from .models import GymVisit
from .serializers import GymVisitSerializer
from django.http import HttpResponse, JsonResponse
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta


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
    # Get current time from Django's timezone (uses settings.TIME_ZONE)
    now = timezone.now()
    
    # Calculate the boundaries for the week (last 7 days) and month (last 30 days)
    week_start = now - timedelta(days=7)
    month_start = now - timedelta(days=30)
    
    # Aggregation: count visits per user within the last week and month.
    week_leaderboard = (
        GymVisit.objects.filter(entry_time__gte=week_start)
        .values('user')
        .annotate(visit_count=Count('id'))
        .order_by('-visit_count')
    )
    
    month_leaderboard = (
        GymVisit.objects.filter(entry_time__gte=month_start)
        .values('user')
        .annotate(visit_count=Count('id'))
        .order_by('-visit_count')
    )
    
    # Prepare the response data as a dictionary
    data = {
        "week_leaderboard": list(week_leaderboard),
        "month_leaderboard": list(month_leaderboard)
    }
    
    # Return the data as JSON
    return JsonResponse(data)
