from django.db import models
from django.contrib.auth.models import User
import json

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return self.user.username
    
class GymVisit(models.Model):
    user = models.CharField(max_length=100)
    entry_time = models.DateTimeField()
    exit_time = models.DateTimeField()
    gym_location = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        # You can return a JSON-like string representation
        return json.dumps({
            "user": self.user,
            "entry_time": self.entry_time.isoformat(),
            "exit_time": self.exit_time.isoformat(),
            "gym_location": self.gym_location
        })
    
    #in case it doesn't work look up __to__JSON
