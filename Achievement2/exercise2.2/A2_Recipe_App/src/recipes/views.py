import base64
from io import BytesIO
from django.urls import reverse

import matplotlib
import matplotlib.pyplot as plt
from django.conf import settings
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import CreateView, DetailView, ListView
from django.utils.html import format_html

import recipes

from .models import CustomUser, Recipe

matplotlib.use("Agg")
import random

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import RecipeForm, RecipeSearchForm


class HomeView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = "recipes/recipes_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_recipes = Recipe.objects.all()
        if len(all_recipes) >= 5:
            random_recipes = random.sample(list(all_recipes), 5)
        else:
            random_recipes = list(all_recipes)
        context["random_suggestions"] = random_recipes
        context["MEDIA_URL"] = settings.MEDIA_URL
        return context

class SearchResultsView(ListView):
    model= Recipe
    template_name = "recipes/recipes_list.html"
    
    def get_queryset(self):  # new
      query_name = self.request.GET.get('recipe_name')
      query_ingredients = self.request.GET.get('ingredients')
        
        # Your search logic goes here, filter the queryset based on the search parameters
        
      queryset = Recipe.objects.filter(name__icontains=query_name, ingredients__icontains=query_ingredients)
        
      return queryset
  
class RecipeDetailView(LoginRequiredMixin, DetailView):
    model = Recipe
    template_name = "recipes/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recipe = self.object
        difficulty = recipe.calc_difficulty()
        context["difficulty"] = difficulty
        context["MEDIA_URL"] = settings.MEDIA_URL
        return context

@login_required
def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    is_liked = request.user.fav_recipes.filter(pk=pk).exists()
    
    context = {
        'recipe': recipe,
        'is_liked': is_liked,
    }

    return render(request, 'recipes/detail.html', context)

class RecipeListView(ListView):
    model = Recipe
    template_name = "recipes/recipes_list.html"
    form = RecipeSearchForm()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_recipes = Recipe.objects.all()
        context["recipes"] = [
          {
            "recipe": recipe,
            "image_url": recipe.pic.url,
            "pk": recipe.pk,
          }
          for recipe in all_recipes
        ]

        # Generate the graph here
        x = [recipe["recipe"].name for recipe in context["recipes"]]
        y = [recipe["recipe"].cooking_time for recipe in context["recipes"]]
        chart = self.get_plot(x, y)
        context["chart"] = chart
        context["MEDIA_URL"] = settings.MEDIA_URL

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
            if recipes:
              return redirect('recipes:detail', pk=recipes[0].pk)
            if not recipes:
                messages.info(self.request, "No recipes found")

            # Update the graph based on the filtered recipes
            x = [recipe.name for recipe in recipes]
            y = [recipe.cooking_time for recipe in recipes]
            chart = self.get_plot(x, y)
            context["chart"] = chart

        return render(self.request, "recipes/recipes_list.html", context)
      
    def get(self, request, *args, **kwargs):
        # Handle the click on the recipe image
        recipe_id = self.request.GET.get('recipe_id')
        if recipe_id:
            return redirect(reverse('recipes:detail', kwargs={'pk': recipe_id[0].pk}))
        else:
            return super().get(request, *args, **kwargs)
          
    def graph_view(request):
        # You can access the chart within the context here
        chart = request.context["chart"]
        return render(request, "recipes/recipes_list.html", {"chart": chart})
      
class Profile(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = "recipes/profile.html"
    context_object_name = "user"
    slug_field = "username"
    slug_url_kwarg = "username"
    
    def get_object(self, queryset=None):
        return get_object_or_404(CustomUser, username=self.kwargs['username'])


class AddRecipe(LoginRequiredMixin, CreateView):
    model = Recipe
    template_name = "recipes/add_recipe.html"
    form_class = RecipeForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["MEDIA_URL"] = settings.MEDIA_URL
        return context


@login_required
def delete_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)

    if request.user == recipe.author:
        if request.method == "POST":
            # Check for a confirmation parameter sent via POST
            if request.POST:
                recipe.delete()
                return redirect("recipes:recipe")
            else:
                return redirect("recipes:detail", pk=recipe_id)
    return redirect("recipes:recipe")


@login_required
def edit_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)

    if request.user == recipe.author:
        if request.method == "POST":
            recipe_form = RecipeForm(request.POST, instance=recipe)
            if recipe_form.is_valid():
                recipe_form.save()
                return redirect("recipes:detail", pk=recipe_id)

    return redirect("recipes:detail", pk=recipe_id)


@login_required
def faved_recipe(request, recipe_id):
    user = request.user
    recipe = get_object_or_404(Recipe, pk=recipe_id)

    if user.fav_recipes.filter(pk=recipe_id).exists():
        user.fav_recipes.remove(recipe)
        is_liked = False
    else:
        user.fav_recipes.add(recipe)
        is_liked = True

    response_data = {
        "is_liked": is_liked,
    }

    return JsonResponse(response_data)


@login_required
def update_profile_picture(request, username):
    if request.method == "POST":
        profile_pic = request.FILES["profile_pic"]
        request.user.pic = profile_pic
        request.user.save()
        print(request.FILES)
        return redirect("recipes:profile", username=request.user.username)
    else:
        return redirect("recipes:profile", username=request.user.username)




   