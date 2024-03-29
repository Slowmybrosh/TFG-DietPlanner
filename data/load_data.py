import csv, json
from app.configuration import Configuration
from app.models import RecipeIngredient, Recipes, Ingredients

RecipeIngredient.objects.all().delete()
Recipes.objects.all().delete()
Ingredients.objects.all().delete()

configuration = Configuration()
# Carga de los datos del CSV
with open(configuration.data_ingredients, "r") as f:
    reader = csv.reader(f, delimiter=",")
    next(reader)
    for row in reader:
        ingredient = Ingredients(id=row[0],name=row[1])
        ingredient.save()

# # Cargar las recetas en formato JSON
with open(configuration.data_recipes, "r", encoding="utf-8") as f:
    recipes = json.load(f)

for recipe in recipes:
    _steps = ";".join(recipe['Steps'])
    row = Recipes(name=recipe['Name'],steps=_steps,number_of_ingredients=None)
    row.save()

for recipe in recipes:
    ingredients = recipe['Ingredients_ID']
    name = recipe['Name']
    resultado = Recipes.objects.get(name=name)
    id = resultado.id

    for ingredient in ingredients:
        result_ingredient = Ingredients.objects.get(id=ingredient)
        recipeingredient = RecipeIngredient(recipe_id=resultado,ingredient_id=result_ingredient)
        recipeingredient.save()

## Actualizar tabla para incluir el número de ingredientes de la receta
for recipe in recipes:
    name = recipe['Name']
    resultado = Recipes.objects.get(name=name)
    id = resultado.id
    num_ingredients = RecipeIngredient.objects.filter(recipe_id=id).count()
    Recipes.objects.filter(id=id).update(number_of_ingredients=num_ingredients)