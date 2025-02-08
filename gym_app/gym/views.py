# gym/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer  # Optional, for explicit JSON rendering
from .models import GymVisit
from .serializers import GymVisitSerializer
from django.http import HttpResponse
from django.http import JsonResponse
from .utils import calculate_average_rating, get_time_based_ratings

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
