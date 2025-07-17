from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignUpForm, LoginForm, ProfileEditForm
from .models import Profile
from core.models import Visit
from core.api import *

# Create your views here.
# ----AUTHENTICATION----
def sign_up_user(request):
    title = "SignUp"
    
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect("account:profile_view", slug=user.slug)
        else:
            messages.error(request, "There was an error. Try again")
    else:
        form = SignUpForm()

    context = {"form": form, "title": title}
    return render(request, "account/login_sign_up.html", context)

def login_user(request):
    title = "Login"
    
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("account:profile_view", slug=user.profile.slug)
        else:
            messages.error(request, "There was an error. Try again")
    
    form = LoginForm()
    context = {"form": form, "title": title}
    return render(request, "account/login_sign_up.html", context)

@login_required
def logout_user(request):
    logout(request)
    return redirect("core:home")


# ----PROFILE----
def profile_view(request, slug):
    profile = get_object_or_404(Profile, slug=slug)
    visits = Visit.objects.filter(profile=profile)
    friends = profile.friends.all()
    is_friend = profile.friends.filter(id=request.user.profile.id).exists()
    countries = []
    for visit in visits:
        if visit.country not in countries:
            countries.append(visit.country)
    for i, country in enumerate(countries):
        country = get_country_info(country)[0]
        if country:
            countries[i] = country
    
    your_chats = profile.user.chat_groups.all()
    context = {"profile": profile, "visits": visits, "countries": countries, "friends": friends,  "is_friend": is_friend, "your_chats": your_chats}
    return render(request, "account/profile_view.html", context)

def profile_edit(request):
    profile = request.user.profile

    if request.method == "POST":
        form = ProfileEditForm(data=request.POST, files=request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("account:profile_view", slug=profile.slug)
    else:
         form = ProfileEditForm(instance=profile)

    context = {"profile": profile, "form": form}
    return render(request, "account/profile_edit.html", context)

@login_required
def add_friend(request, slug):
    profile = request.user.profile
    friend_to_add = get_object_or_404(Profile, slug=slug)

    if friend_to_add.user not in profile.friends.all():
        profile.friends.add(friend_to_add.user)
    else:
        profile.friends.remove(friend_to_add.user)
    

    return redirect("account:profile_view", slug=friend_to_add.slug)