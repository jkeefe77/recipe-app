from django.urls import path
from .views import recipes_home
from .views import RecipeListView
from .views import RecipeDetailView
from . import views

app_name = "recipes"

urlpatterns = [
    path("", recipes_home, name="home"),
    path('recipes/', views.recipe_list, name='recipe-list'),
    path("list/", RecipeListView.as_view(), name="list"),
    path("list/<pk>", RecipeDetailView.as_view(), name="detail"),
]
