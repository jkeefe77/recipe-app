from django.test import TestCase

# Create your tests here.
from .models import Recipe

# Create your tests here.


class RecipeModelTest(TestCase):
    def setUpTestData():
        # Set up non-modified object used by all test methods
        Recipe.objects.create(
            recipe_id=1,
            name="Pizza",
            cooking_time=30,
            difficulty="Recipe.HARD",
            ingredients="cheese, tomato sauce, dough",
            description="A classic take on a traditional Italian favorite",
        )

    # Test Recipe Name

    def test_recipe_name(self):
        recipe = Recipe.objects.get(recipe_id=1)

        # Get metadata for the 'name' field to query its data

        field_label = recipe._meta.get_field("name").verbose_name

        # Compare the value to the expected result

        self.assertEqual(field_label, "name")

    # Test cooking time for time limit

    def test_cooking_time__max_value(self):
        # Get a recipe object to test
        recipe = Recipe.objects.get(recipe_id=1)

        # Ensure cooking time does not exceed 60 mins
        self.assertLessEqual(recipe.cooking_time, 60)

    def test_max_ingredients_limit(self):
        # Get a recipe object to test
        recipe = Recipe.objects.get(recipe_id=1)

        self.assertLessEqual(len(recipe.ingredients.split()), 10)

        # Test description field for max characters

    def test_description_max_length(self):
        # Get a recipe object to test
        recipe = Recipe.objects.get(recipe_id=1)

        # Ensure that the description does not exceed 500 characters
        self.assertLessEqual(len(recipe.description), 500)
