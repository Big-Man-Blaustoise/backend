from django.contrib import admin

from gym.models import Profile
from .models import GymVisit
from .forms import GymVisitAdminForm


# Register your models here.
admin.site.register(Profile)


@admin.register(GymVisit)
class GymVisitAdmin(admin.ModelAdmin):
    form = GymVisitAdminForm
    list_display = ['user', 'entry_time', 'gym_location', 'gym_busy_rating']  # Fields to display in the list
    search_fields = ['user', 'gym_location']  # Fields to search by