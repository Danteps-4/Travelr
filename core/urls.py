from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("visit/add/country/<str:name>/", views.visit_country_add, name="visit_country_add"),
    path("visit/edit/<slug:slug>/", views.visit_edit, name="visit_edit"),
    path("visit/delete/<slug:slug>/", views.visit_delete, name="visit_delete"),
]
