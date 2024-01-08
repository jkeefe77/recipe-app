from django.urls import path
from .views import HomeView, RecipeListView, RecipeDetailView, Profile, faved_recipe, SearchResultsView




app_name = "recipes"

urlpatterns = [
    path("home/", HomeView.as_view(), name="home"),
    path("search_results/", SearchResultsView.as_view(), name="search_results"),
    path("recipes/", RecipeListView.as_view(), name="recipes"),
    path("list/", RecipeListView.as_view(), name="list"),
    path("detail/<pk>", RecipeDetailView.as_view(), name="detail"),
    path("profile/<slug:username>/", Profile.as_view(), name="profile"),
    path('faved_recipe/<int:recipe_id>/', faved_recipe, name='faved_recipe')
]
