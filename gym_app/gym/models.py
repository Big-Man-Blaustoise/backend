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
    # Change the user field to reference the User model.
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    entry_time = models.DateTimeField()
    exit_time = models.DateTimeField()
    gym_location = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        # Return a JSON-like representation, showing the user's username.
        return json.dumps({
            "user": self.user.username,
            "entry_time": self.entry_time.isoformat(),
            "exit_time": self.exit_time.isoformat(),
            "gym_location": self.gym_location
        })