# gym_app/serializers.py
from rest_framework import serializers
from gym.models import GymVisit

class GymVisitSerializer(serializers.ModelSerializer):
    # Explicitly format both datetime fields
    entry_time = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%SZ')
    
    class Meta:
        model = GymVisit
        fields = ['user', 'entry_time', 'gym_location', 'gym_busy_rating']
