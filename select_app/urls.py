from django.urls import path
from . import views

app_name = "select"

urlpatterns = [
    path("", views.select, name="select"),
]