from django.urls import path, include
from .views import HomeView
from .views import RecipeListView
from .views import RecipeDetailView
from . import views


app_name = "recipes"

urlpatterns = [
    path("home/", HomeView.as_view(), name="home"),
    path("recipes/", RecipeListView.as_view(), name="recipes"),
    path("list/", RecipeListView.as_view(), name="list"),
    path("list/<pk>", RecipeDetailView.as_view(), name="detail"),
]
