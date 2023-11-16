from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.contrib import messages
from .models import Recipe
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .forms import RecipeForm, RecipeSearchForm
from django.contrib.auth.models import User
import pandas as pd
from django.db.models import Q
import matplotlib.pyplot as plt
import base64
from io import BytesIO


# Create your views here.


class HomeView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = "recipes/recipes_home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_recipes = Recipe.objects.all()
        if len(all_recipes) >= 5:
            random_recipes = random.sample(list(all_recipes), 5)
        else:
            random_recipes = list(all_recipes)
        context["random_suggestions"] = random_recipes
        return context


class RecipeDetailView(LoginRequiredMixin, DetailView):
    model = Recipe
    template_name = "recipes/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recipe = self.object
        difficulty = recipe.calc_difficulty()
        context["difficulty"] = difficulty
        return context


class RecipeListView(ListView):
    model = Recipe
    template_name = "recipes/recipes_list.html"
    form = RecipeSearchForm()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_recipes = Recipe.objects.all()
        context["recipes"] = all_recipes

        # Generate the graph here
        x = [recipe.name for recipe in all_recipes]
        y = [recipe.cooking_time for recipe in all_recipes]
        chart = self.get_plot(x, y)
        context["chart"] = chart

        return context

    def get_plot(self, x, y):
        buffer = BytesIO()
        plt.switch_backend("AGG")
        plt.figure(figsize=(10, 5))
        plt.title("Recipe Chart")
        plt.bar(x, y)
        plt.xticks(rotation=45)
        plt.xlabel("Recipes")
        plt.ylabel("Cooking Time")
        plt.tight_layout()
        plt.savefig(buffer, format="png")
        buffer.seek(0)
        image_png = buffer.getvalue()
        graph = base64.b64encode(image_png).decode("utf-8")
        buffer.close()
        return graph

    def post(self, request, *args, **kwargs):
        form = RecipeSearchForm(self.request.POST)

        if form.is_valid():
            recipe_name = form.cleaned_data["recipe_name"]
            ingredients = form.cleaned_data["ingredients"]

            recipes = Recipe.objects.all()

            if recipe_name:
                recipes = recipes.filter(Q(name__icontains=recipe_name))

            if ingredients:
                recipes = recipes.filter(Q(ingredients__icontains=ingredients))

            if not recipe_name and not ingredients:
                recipes = Recipe.objects.all()

            context = {
                "recipes": recipes,
                "form": form,
            }

            if not recipes:
                messages.info(self.request, "No recipes found")

            # Update the graph based on the filtered recipes
            x = [recipe.name for recipe in recipes]
            y = [recipe.cooking_time for recipe in recipes]
            chart = self.get_plot(x, y)
            context["chart"] = chart

            return render(self.request, "recipes/recipes_list.html", context)

    def graph_view(request):
        # You can access the chart within the context here
        chart = request.context["chart"]
        return render(request, "recipes/recipes_list.html", {"chart": chart})

    def recipes_home(request):
        return render(request, "recipes/recipes_home.html")
