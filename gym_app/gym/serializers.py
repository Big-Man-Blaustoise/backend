# gym_app/serializers.py
from rest_framework import serializers
from gym.models import GymVisit, Profile

class GymVisitSerializer(serializers.ModelSerializer):
    # Explicitly format both datetime fields
    entry_time = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%SZ')
    exit_time = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%SZ')

    class Meta:
        model = GymVisit
        fields = ['user', 'entry_time', 'exit_time', 'gym_location']

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user', 'bio', 'profile_picture']  # Include only necessary fields
