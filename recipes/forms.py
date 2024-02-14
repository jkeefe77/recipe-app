from django import forms  # import django forms
from .models import recipe_genre_choices

CHART__CHOICES = (  # specify choices as a tuple
    # when user selects "Bar chart", it is stored as "#1"
    ('#1', 'Genre Percentage of All Recipes'),
    ('#2', 'Genre Average Rating'),
    ('#3', 'Genre Average Cooking Time')
)

# define class-based Form imported from Django forms


class RecipeChartForm(forms.Form):
    chart_type = forms.ChoiceField(choices=CHART__CHOICES, required=False)

class CreateRecipeForm(forms.Form):
    name = forms.CharField(max_length=50)
    cooking_time = forms.IntegerField(help_text='in minutes')
    genre = forms.ChoiceField(choices=recipe_genre_choices)
    ingredients = forms.CharField(max_length=300)
    rating = forms.FloatField(max_value=10)
    # pic = forms.ImageField(required=False)