from django.urls import path
from . import views

app_name = "visualize"

urlpatterns = [
    path("", views.visualize, name="visualize"),
]