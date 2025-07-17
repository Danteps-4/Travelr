from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .api import *
from .forms import VisitForm
from .models import Visit

# Create your views here.
def home(request):
    return render(request, "core/home.html")

@login_required
def visit_country_add(request, name):
    country = get_country_info(name)[0]
    if request.method == "POST":
        form = VisitForm(request.POST)
        if form.is_valid():
            form.save(True, request, country)
            return redirect("explore:explore")
    else:
        form = VisitForm()
    context = {"country": country, "form": form}
    return render(request, "core/partials/visit_country_add.html", context)

@login_required
def visit_edit(request, slug):
    visit = get_object_or_404(Visit, slug=slug)

    if request.method == "POST":
        form = VisitForm(request.POST, instance=visit)
        if form.is_valid():
            visit = form.save(commit=False)
            visit.profile = request.user.profile
            form.save()
            return redirect("account:profile_view", slug=request.user.profile.slug)
    else:
        form = VisitForm(instance=visit)

    context = {"visit": visit, "form": form}
    return render(request, "core/partials/visit_edit.html", context)

@login_required
def visit_delete(request, slug):
    visit = get_object_or_404(Visit, slug=slug)
    
    if request.user.profile != visit.profile:
        return redirect("account:profile_view", slug=request.user.profile.slug)
    
    visit.delete()
    return redirect("account:profile_view", slug=request.user.profile.slug)