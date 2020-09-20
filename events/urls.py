from django.urls import path
from . import views

urlpatterns = [
    path('rides/', views.rides, name="rides"),
    path('events/', views.event, name="events"),
    path('reg_to_event/', views.registered_to_event_chart, name="reg_to_event"),
    path('reg_to_ride/', views.registered_to_ride_chart, name="reg_to_ride"),
    path('gallery/', views.gallery, name="gallery"),
]