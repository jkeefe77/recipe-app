from django.db import models

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

    difficulty = models.CharField(
        max_length=60,
        choices=DIFFICULTY_CHOICES,
        default=BEGINNER,
    )

    def save(self, *args, **kwargs):
        force_insert = kwargs.pop("force_insert", False)
        super(Recipe, self).save(*args, **kwargs)
        # Adjust these thresholds as needed based on your criteria
        if self.cooking_time <= 30 and len(self.ingredients.split()) <= 5:
            self.difficulty = self.BEGINNER
        elif self.cooking_time <= 60 and len(self.ingredients.split()) <= 10:
            self.difficulty = self.INTERMEDIATE
        else:
            self.difficulty = self.HARD

    def __str__(self):
        return str(self.name)
