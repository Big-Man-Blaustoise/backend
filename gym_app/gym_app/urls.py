"""
URL configuration for gym_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from gym.views import GymVisitList, home, leaderboard, profile_detail
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken import views as auth_views

urlpatterns = [
    path('api/', home, name='home'),  # Render the home view for the root URL
    path('api/admin/', admin.site.urls),
    path('api/gym-visits/', GymVisitList.as_view(), name='gym-visit-list'),
    path('api/leaderboard/', leaderboard, name='leaderboard'),
    path('api/profiles/<str:username>/', profile_detail, name='profile_detail'),
    # REST Framework auth endpoints
    path('api/auth/', include('rest_framework.urls')),  # Browsable API auth
    path('api/auth/token/', auth_views.obtain_auth_token, name='api_token_auth'),  # Token generation endpoint
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)