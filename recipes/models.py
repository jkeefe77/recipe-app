from django.db import models
from django.shortcuts import reverse

# Create your models here.

recipe_genre_choices = (
    ('appetizer', 'Appetizer'),
    ('entree', 'Entree'),
    ('drink', 'Drink'),
    ('dessert', 'Dessert'),
    ('snack', 'Snack'),
    ('other', 'Other')
)


class Recipe(models.Model):
    name = models.CharField(max_length=50)
    cooking_time = models.PositiveIntegerField(help_text='in minutes')
    genre = models.CharField(
    max_length=20, choices=recipe_genre_choices, default='other')
    ingredients = models.TextField(max_length=300)
    pic = models.ImageField(upload_to='recipes', default='no_picture.jpg')

    # calculate difficulty of recipe using cooking time and number of ingredients
    def calculate_difficulty(self):
        ingredients = self.ingredients.split(', ')
        if self.cooking_time < 25 and len(ingredients) < 6:
            difficulty = 'Easy'
        elif self.cooking_time < 25 and len(ingredients) >= 6:
            difficulty = 'Medium'
        elif self.cooking_time >= 25 and len(ingredients) < 6:
            difficulty = 'Intermediate'
        elif self.cooking_time >= 25 and len(ingredients) >= 6:
            difficulty = 'Hard'
        return difficulty

    # returns the url of the individual recipe detail page
    def get_absolute_url(self):
        return reverse('recipes:detail', kwargs={'pk': self.pk})

    def __str__(self):
        return str(self.name)
