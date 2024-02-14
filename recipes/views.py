from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Recipe
# to protect class-based view
from django.contrib.auth.mixins import LoginRequiredMixin
# to protect class-based view
from django.contrib.auth.decorators import login_required
from .forms import RecipeChartForm, CreateRecipeForm
import pandas as pd
from .utils import get_chart
from django.core.files.uploadedfile import SimpleUploadedFile

# Create your views here.


def welcome_view(request):
    return render(request, 'recipes/welcome.html')


def about_view(request):
    return render(request, 'recipes/about.html')


class RecipeListView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = 'recipes/list.html'


class RecipeDetailView(LoginRequiredMixin, DetailView):
    model = Recipe
    template_name = 'recipes/detail.html'


# @login_required
def create_view(request):
    create_form = CreateRecipeForm(request.POST or None, request.FILES)
    name = None
    cooking_time = None
    genre = None
    ingredients = None
    rating = None
    # pic = None

    if request.method == 'POST':

        try:
            recipe = Recipe.objects.create(
                name = request.POST.get('name'),
                cooking_time = request.POST.get('cooking_time'),
                genre = request.POST.get('genre'),
                ingredients = request.POST.get('ingredients'),
                rating = request.POST.get('rating'),
                # pic = request.POST.get('pic')
            )

            recipe.save()

        except:
            print('Error!!!')

    context = {
        'create_form': create_form,
        'name': name,
        'cooking_time': cooking_time,
        'genre': genre,
        'ingredients': ingredients,
        'rating': rating,
        # 'pic': pic
    }

    return render(request, 'recipes/create.html', context)


@login_required
def records_view(request):

    # create an instance of RecipeChartForm that you defined in recipes/forms.py
    chart_form = RecipeChartForm(request.POST or None)
    recipe_df = None  # initialize dataframe to None
    chart = None  # initialize chart to None
    qs = None

    # check if the button is clicked
    if request.method == 'POST':
        chart_type = request.POST.get('chart_type')  # read recipe chart type
        if not chart_type:
            chart_type = '#1'

        # apply filter to extract data
        qs = Recipe.objects.all()

        if qs:  # if the data is found, convert the queryset values to pandas dataframe
            recipe_df = pd.DataFrame(qs.values())
            chart = get_chart(chart_type, recipe_df)

            recipe_df = pd.DataFrame(qs.values(), columns=['id', 'name', 'cooking_time', 'genre', 'ingredients'])

            links = []

            for e, nam in enumerate(recipe_df['name']):
                nam = '<a href="/detail/' + str(recipe_df['id'][e]) + '">' + str(nam) + '</a>'
                links.append(nam)

            recipe_df['name'] = links

            # convert the dataframe to HTML
            recipe_df = recipe_df.to_html(index=False, escape=False)



    # print(recipe_genre)
    # pack up data to be sent to template in the context dictionary
    context = {
        'chart_form': chart_form,
        'recipe_df': recipe_df,
        'chart': chart,
        'qs': qs,
    }

    # load the template and send the context dictionary to template
    return render(request, 'recipes/records.html', context)
