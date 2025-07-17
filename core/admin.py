from django.contrib import admin
from .models import Visit

# Register your models here.
@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ["profile", "country", "date_from", "date_until"]