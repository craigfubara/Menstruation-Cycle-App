from django.urls import path
from . import views

urlpatterns = [
    path('tracker/calendar-data/', views.calendar_data, name='api_calendar_data'),
]
