import pickle

recipes_list = []
ingredients_list = []


def calc_difficulty(cooking_time, ingredients):
    if cooking_time < 10 and len(ingredients) < 4:
        difficulty = "easy"
        return difficulty
    elif cooking_time < 10 and len(ingredients) >= 4:
        difficulty = "medium"
        return difficulty
    elif cooking_time >= 10 and len(ingredients) < 4:
        difficulty = "intermediate"
        return difficulty
    elif cooking_time >= 10 and len(ingredients) >= 4:
        difficulty = "hard"
        return difficulty


def take_recipe():
    name = str(input("Enter the name of the recipe: "))
    cooking_time = int(input("Enter the cooking time in minutes: "))
    ingredients_input = str(
        input(
            "Enter all the ingredients required for the recipe - each one being separated by a comma following by a space (bread, cheese...)): "
        )
    )
    ingredients = ingredients_input.split(", ")
    difficulty = calc_difficulty(cooking_time, ingredients)
    recipe = {
        "name": name,
        "cooking_time": cooking_time,
        "ingredients": ingredients,
        "difficulty": difficulty,
    }
    return recipe


recipe_file_name = (
    str(input("Enter the filename for which you would like to store your recipe(s): "))
    + ".bin"
)

try:
    recipe_file = open(recipe_file_name, "rb")
    data = pickle.load(recipe_file)
except FileNotFoundError:
    print("The file with the given name isn’t found")
    data = {"Recipes list": recipes_list, "Ingredients list": ingredients_list}
except:
    print("Oops, we've stumbled on some unexpected error.")
    data = {"Recipes list": recipes_list, "Ingredients list": ingredients_list}
else:
    recipe_file.close()
finally:
    recipes_list = data["Recipes list"]
    print("This file already contains the following recipes: " + str(recipes_list))
    ingredients_list = data["Ingredients list"]
    print("and this list of ingredients: " + str(ingredients_list))

number_of_recipes = int(input("Enter how many recipe(s) you would like to create: "))
n = number_of_recipes

for number_recipe_specified in range(n):
    recipe = take_recipe()
    recipes_list.append(recipe)
    for ingredient in recipe["ingredients"]:
        if not ingredient in ingredients_list:
            ingredients_list.append(ingredient)

print("This is the updated recipe file, with the new added recipe(s): " + str(data))

recipe_file = open(recipe_file_name, "wb")
pickle.dump(data, recipe_file)
recipe_file.close()
