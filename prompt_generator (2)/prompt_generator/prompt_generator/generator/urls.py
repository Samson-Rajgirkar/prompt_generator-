"""generator app URL configuration."""

from django.urls import path
from . import views

app_name = 'generator'

urlpatterns = [
    # Main page
    path('', views.index, name='index'),

    # History page
    path('history/', views.history, name='history'),

    # Feedback endpoint (AJAX)
    path('feedback/<int:prompt_id>/', views.submit_feedback, name='submit_feedback'),

    # JSON API
    path('api/classify/', views.api_classify, name='api_classify'),
]
