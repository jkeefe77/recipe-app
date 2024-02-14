from django.test import TestCase
from .models import Recipe
from .forms import RecipeChartForm

# Create your tests here.


class RecipeModelTest(TestCase):
    def setUpTestData():
        # Set up non-modified objects used by all test methods
        Recipe.objects.create(
            name='Tasty Cito Salsa',
            cooking_time=9,
            ingredients=['tomato', 'onion', 'jalepeno'],
        )

    def test_recipe_name(self):
        # Get a recipe object to test
        ing = Recipe.objects.get(id=1)

        # Get the metadata for the 'name' field and use it to query its data
        field_label = ing._meta.get_field('name').verbose_name

        # Compare the value to the expected result
        self.assertEqual(field_label, 'name')

    def test_recipe_name_max_length(self):
        # Get a recipe object to test
        ing = Recipe.objects.get(id=1)

        # Get the metadata for the 'name' field and use it to query its max_length
        max_length = ing._meta.get_field('name').max_length

        # Compare the value to the expected result i.e. 50
        self.assertEqual(max_length, 50)

    def test_recipe_pic_upload_to(self):
        upload_to = Recipe._meta.get_field("pic").upload_to
        self.assertEqual(upload_to, "recipes")

    def test_get_absolute_url(self):
        recipe = Recipe.objects.get(id=1)
        # get_absolute_url() should load the URL /recipes/detail/1
        self.assertEqual(recipe.get_absolute_url(), '/detail/1')


class RecipeChartFormTest(TestCase):

    def test_form_renders_chart_type_input(self):
        form = RecipeChartForm()
        self.assertIn('chart_type', form.as_p())

    def test_form_valid_data(self):
        form = RecipeChartForm(
            data={'chart_type': '#2'})
        self.assertTrue(form.is_valid())

    def test_form_invalid_data(self):
        form = RecipeChartForm(data={'chart_type': ''})
        self.assertFalse(not form.is_valid())
