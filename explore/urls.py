from django.urls import path
from . import views

app_name = "explore"

urlpatterns = [
    path("", views.explore, name="explore"),
    path("country/<str:name>/", views.country, name="country"),
]
