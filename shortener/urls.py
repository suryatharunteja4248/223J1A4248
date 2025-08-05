from django.urls import path
from .views import create_short_url, redirect_url, get_stats

urlpatterns = [
    path('shorturls', create_short_url),                # Q2 POST
    path('shorturls/<str:shortcode>', get_stats),       # Q3 GET
    path('<str:shortcode>', redirect_url),              # Q1 Redirect
]
