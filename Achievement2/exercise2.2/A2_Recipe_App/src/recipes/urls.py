from django.urls import path, include
from .views import HomeView
from .views import RecipeListView, RecipeDetailView, HomeView, Profile
from . import views


app_name = "recipes"

urlpatterns = [
    path("home/", HomeView.as_view(), name="home"),
    path("recipes/", RecipeListView.as_view(), name="recipes"),
    path("list/", RecipeListView.as_view(), name="list"),
    path("list/<pk>", RecipeDetailView.as_view(), name="detail"),
    path("profile/<slug:username>/", Profile.as_view(), name="profile"),
    path(
        "profile/<slug:username>/update/",
        views.update_profile_picture,
        name="update_profile_picture",
    ),
]
