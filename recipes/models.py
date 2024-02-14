from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import AbstractUser, Group, Permission

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

class CustomUser(AbstractUser):
    # Add custom fields to your user model
    pic = models.ImageField(
        upload_to="profile_pics", blank=True, null=True, default="no_picture.jpg"
    )
    bio = models.TextField(blank=True, null=True)
    fav_recipes = models.ManyToManyField(
        Recipe, blank=True, related_name="users_favorites"
    )
    groups = models.ManyToManyField(
        Group, verbose_name="groups", blank=True, related_name="customuser_groups"
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name="user permissions",
        blank=True,
        related_name="customuser_permissions",
    )

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse("recipes:profile", kwargs={"username": self.username})