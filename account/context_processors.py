from django.shortcuts import get_object_or_404
from .models import Profile
from core.models import Visit


def avatar(request):
    if request.user.is_authenticated:
        return {'avatar': request.user.profile.avatar.url}
    return {'avatar': '/media/profile_pics/default.png'}

def world_percentage(request):
    TOTAL_COUNTRIES = 253
    slug = request.resolver_match.kwargs.get("slug", None) if request.resolver_match else None

    if not slug:
        return {"countries_visited": 0, "world_percentage": 0}

    profile = get_object_or_404(Profile, slug=slug)
    visits = Visit.objects.filter(profile=profile)

    countries_visited = {visit.country for visit in visits}  # Usamos set para evitar duplicados
    visited_count = len(countries_visited)

    return {
        "countries_visited": visited_count,
        "world_percentage": (visited_count / TOTAL_COUNTRIES) * 100,
    }
