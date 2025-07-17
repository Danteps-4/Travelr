from django.shortcuts import render
from core.models import Visit
from core.api import *

# Create your views here.
def visualize(request):
    countries = []
    if (request.user.is_authenticated):
        profile = request.user.profile
        visits = Visit.objects.filter(profile=profile)
        for visit in visits:
            if visit.country not in countries:
                countries.append(get_country_info(visit.country)[0]["cca3"])
    
    context = {"countries": countries}
    return render(request, "visualize/visualize.html", context)