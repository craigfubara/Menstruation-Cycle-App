from django.urls import path
from . import views

app_name = 'App_Tracker'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('log-period/', views.log_period, name='log_period'),
    path('daily-log/', views.daily_log, name='daily_log'),
    path('pain-management/', views.pain_management, name='pain_management'),
    path('history/', views.cycle_history, name='cycle_history'),
    path('settings/', views.settings_view, name='settings'),
    path('calendar-data/', views.calendar_data, name='calendar_data'),
]
