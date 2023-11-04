import csv, json
from db import Db_connector
from sqlalchemy import select, update
from sqlalchemy.inspection import inspect
from decouple import config
from models import Base, Recipes, RecipeIngredient,Ingredient

# Conexión con la base de datos
db = Db_connector(config("DB_NAME"))

if inspect(db._engine).has_table("ingredients"):
    Base.metadata.drop_all(db._engine)

if not inspect(db._engine).has_table("ingredients"):
    Base.metadata.create_all(db._engine)

# Carga de los datos del CSV
with open("./data/ingredients.csv", "r") as f:
    reader = csv.reader(f, delimiter=",")
    next(reader)
    for row in reader:
        ingredient = Ingredient(id=row[0],name=row[1])
        db._session.add(ingredient)
        db._session.commit()

# # Cargar las recetas en formato JSON
with open("./data/recipes.json", "r", encoding="utf-8") as f:
    recipes = json.load(f)

for recipe in recipes:
    _steps = ";".join(recipe['Steps'])
    row = Recipes(name=recipe['Name'],steps=_steps,numberofingredients=None)
    db._session.add(row)
    db._session.commit()

for recipe in recipes:
    ingredients = recipe['Ingredients_ID']
    name = recipe['Name']
    resultado = db._session.execute(select(Recipes).where(Recipes.name == name)).first()
    id = resultado[0].id
    for ingredient in ingredients:
        recipeingredient = RecipeIngredient(recipe_id=id,ingredient_id=ingredient)
        db._session.add(recipeingredient)
        db._session.commit()

# # Actualizar tabla para incluir el número de ingredientes de la receta
for recipe in recipes:
    name = recipe['Name']
    resultado = db._session.execute(select(Recipes).where(Recipes.name == name)).first()
    id = resultado[0].id
    resultado = db._session.execute(select(RecipeIngredient).where(RecipeIngredient.recipe_id == id))
    _numberofingredients = len(resultado.fetchall())
    db._session.execute(update(Recipes).where(Recipes.id == id).values(numberofingredients = _numberofingredients))
    db._session.commit()

db._session.close()