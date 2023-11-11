from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Recipe
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required


# Create your views here.
class RecipeListView(ListView, LoginRequiredMixin):
    model = Recipe
    template_name = "recipes/recipes_list.html"


class RecipeDetailView(DetailView, LoginRequiredMixin):
    model = Recipe
    template_name = "recipes/detail.html"


def recipes_home(request):
    return render(request, "recipes/recipes_home.html")


def recipe_detail(request, pk):
    recipe = Recipe.objects.get(pk=pk)
    return render(request, "recipes/detail.html", {"recipe": recipe})


def recipe_list(request):
    recipes = Recipe.objects.all()  # Retrieve all recipes from the database
    return render(request, "recipes/recipe_list.html", {"object_list": recipes})
