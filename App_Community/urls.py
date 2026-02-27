from django.urls import path
from . import views

app_name = 'App_Community'

urlpatterns = [
    path('', views.story_list, name='story_list'),
    path('share/', views.share_story, name='share_story'),
    path('story/<slug:slug>/', views.story_detail, name='story_detail'),
    path('react/<int:pk>/<str:reaction_type>/', views.react_to_story, name='react'),
]
