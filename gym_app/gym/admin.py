from django.contrib import admin

from gym.models import Profile
from .models import GymVisit
from .forms import GymVisitAdminForm


# Register your models here.
admin.site.register(Profile)


@admin.register(GymVisit)
class GymVisitAdmin(admin.ModelAdmin):
    form = GymVisitAdminForm