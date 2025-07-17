from django.urls import path
from . import views

app_name = "account"

urlpatterns = [
    path("login/", views.login_user, name="login"),
    path("sign-up/", views.sign_up_user, name="sign_up"),
    path("logout/", views.logout_user, name="logout"),

    # Profile
    path("profile/edit/", views.profile_edit, name="profile_edit"),
    path("profile/<slug:slug>/", views.profile_view, name="profile_view"),

    path("profile/add_friend/<slug:slug>/", views.add_friend, name="add_friend"),
]
