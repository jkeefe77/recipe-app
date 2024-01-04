from django.urls import path
from .views import HomeView, RecipeListView, RecipeDetailView, Profile, faved_recipe



app_name = "recipes"

urlpatterns = [
    path("home/", HomeView.as_view(), name="home"),
    path("recipes/", RecipeListView.as_view(), name="recipes"),
    path("list/", RecipeListView.as_view(), name="list"),
    path("list/<pk>", RecipeDetailView.as_view(), name="detail"),
    path("profile/<slug:username>/", Profile.as_view(), name="profile"),
    path('faved_recipe/<int:recipe_id>/', faved_recipe, name='faved_recipe')
]
