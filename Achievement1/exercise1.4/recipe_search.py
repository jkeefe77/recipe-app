import pickle


def display_recipe(recipes):
    if len(recipes) > 0:
        first_recipe = recipes[0]
        print("Recipe: " + first_recipe["name"])
        print("Cooking Time: " + str(first_recipe["cooking_time"]))
        print("Ingredients: " + ", ".join(first_recipe["ingredients"]))
        print("Difficulty: " + first_recipe["difficulty"])
    else:
        print("No recipes to display.")


def search_ingredient(data):
    print("Available Ingredients:")

    for index, ingredient in enumerate(data["Ingredients list"], start=1):
        print(str(index) + ". " + ingredient)

    try:
        # The - 1 at the end is important to adjust the pick for 0-based indexing
        number_from_list = int(input("Pick a number from the list: ")) - 1
        ingredient_searched = number_from_list
    except:
        print("The input is incorrect.")
    else:
        ingredients_list = data["Ingredients list"]
    if 0 <= number_from_list < len(ingredients_list):
        ingredient_searched = ingredients_list[number_from_list]

        for recipe in data["Recipes list"]:
            if ingredient_searched in recipe["ingredients"]:
                print("Recipe: " + recipe["name"])
                print("Cooking Time: " + str(recipe["cooking_time"]))
                print("Ingredients: " + ", ".join(recipe["ingredients"]))
                print("Difficulty: " + recipe["difficulty"])
    else:
        print("Please choose a correct number from the list.")


recipe_file_name = str(
    input("Enter the name of the file that contains your recipe(s): ")
)

try:
    recipe_file = open(recipe_file_name + ".bin", "rb")
    data = pickle.load(recipe_file)
except FileNotFoundError:
    print("The file with the given name has not been found")
else:
    search_ingredient(data)
