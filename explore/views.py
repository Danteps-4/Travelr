from django.shortcuts import render
from core.api import *

# Create your views here.
def explore(request):
    q = request.GET.get("q") if request.GET.get("q") != None else ""
    continents = []

    if q == "":
        countries = get_all_countries()
        continents = ["Africa", "Asia", "Europe", "South America", "North America", "Oceania", "Antarctica"]
    else:
        countries = get_country_info(q)
        for country in countries:
            for continent in country["continents"]:
                if continent not in continents:
                    continents.append(continent)

    context = {"countries": countries, "continents": continents}
    return render(request, "explore/explore.html", context)

def country(request, name):
    country = get_country_info(name)[0]
    lat = country["latlng"][0]
    lng = country["latlng"][1]

    context = {"country": country, "lat": lat, "lng": lng}
    return render(request, "explore/country.html", context)