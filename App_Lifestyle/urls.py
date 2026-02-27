from django.urls import path
from . import views

app_name = 'App_Lifestyle'

urlpatterns = [
    path('', views.recommendations, name='recommendations'),
]
