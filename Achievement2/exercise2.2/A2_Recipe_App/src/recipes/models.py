import logging
from django.conf import settings
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.urls import reverse


# Create your models here.


class Recipe(models.Model):
    BEGINNER = "Beginner"
    INTERMEDIATE = "Intermediate"
    HARD = "HARD"

    DIFFICULTY_CHOICES = [
        (BEGINNER, "Beginner"),
        (INTERMEDIATE, "Intermediate"),
        (HARD, "Hard"),
    ]

    recipe_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=120)
    cooking_time = models.PositiveBigIntegerField(default=60)
    ingredients = models.TextField(default="")
    description = models.TextField(default="")
    pic = models.ImageField(upload_to="recipes", default="no_pic.jpg")

    difficulty = models.CharField(
        max_length=60,
        choices=DIFFICULTY_CHOICES,
        default=BEGINNER,
    )

    def __str__(self):
        return f"""
        {self.name}
        Ingredients: {self.ingredients}
        Cooking Time: {self.cooking_time} minutes
        Difficulty: {self.calc_difficulty()}
        """

    def calc_difficulty(self):
        difficulty_levels = {
            "Easy": "Easy",
            "Medium": "Medium",
            "Intermediate": "Intermediate",
            "Hard": "Hard",
        }

        ingredients_list = self.ingredients.split(", ")
        num_ingredients = len(ingredients_list)

        if self.cooking_time < 10:
            if num_ingredients < 4:
                difficulty = difficulty_levels.get("Easy")
            else:
                difficulty = difficulty_levels.get("Medium")
        else:
            if num_ingredients < 4:
                difficulty = difficulty_levels.get("Intermediate")
            else:
                difficulty = difficulty_levels.get("Hard")

            # Log the difficulty level
            logging.info(f"Recipe difficulty for {self.name}: {difficulty}")

        return difficulty

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        self.ingredients = self.ingredients.title()
        super(Recipe, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("recipes:detail", kwargs={"pk": self.pk})


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
