import sqlite3, csv, json, os
from decouple import config

# Conexión con la base de datos
conn = sqlite3.connect(config("DB_NAME"))

# Creación de las tablas
cursor = conn.cursor()

# Resetear tablas
cursor.execute('DROP TABLE IF EXISTS Ingredients')
cursor.execute('DROP TABLE IF EXISTS Recipes')
cursor.execute('DROP TABLE IF EXISTS RecipeIngredient')
conn.commit()

# Cambiar configuración de la base de datos
cursor.execute("PRAGMA case_sensitive_like=OFF;")
cursor.execute("PRAGMA encoding='UTF-8';")
conn.commit()

cursor.execute(
    '''CREATE TABLE IF NOT EXISTS Ingredients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    );''')

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS Recipes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(255),
        steps TEXT,
        numberofingredients INTEGER
    )
    """
)

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS RecipeIngredient(
        recipe_id INTEGER,
        ingredient_id INTEGER,
        FOREIGN KEY (recipe_id) REFERENCES Recipes(id),
        FOREIGN KEY (ingredient_id) REFERENCES Ingredients(id),
        PRIMARY KEY (recipe_id, ingredient_id)
    )
    """
)

# Carga de los datos del CSV
with open("./data/ingredients.csv", "r") as f:
    reader = csv.reader(f, delimiter=",")
    next(reader)
    for row in reader:
        id = int(row[0])
        ingredient = row[1]
        cursor.execute(
            """
            INSERT INTO Ingredients (id, name)
            VALUES (?, ?)
            """,
            (id, str(ingredient))
        )

# Cargar las recetas en formato JSON
with open("./data/recipes.json", "r", encoding="utf-8") as f:
    recipes = json.load(f)

for recipe in recipes:
    name = recipe['Name']
    ingredients = recipe['Ingredients_ID']
    steps = ";".join(recipe['Steps'])
    cursor.execute(
        """
        INSERT INTO Recipes (name,steps,numberofingredients)
        VALUES (?,?,?);
        """,
        (name,steps,None)
    )

conn.commit()

for recipe in recipes:
    ingredients = recipe['Ingredients_ID']
    name = recipe['Name']
    cursor.execute(
        f"""
        SELECT id FROM recipes WHERE name = '{name}'
        """
    )
    id = cursor.fetchone()
    for ingredient in ingredients:
        cursor.execute(
            """
            INSERT INTO RecipeIngredient (recipe_id,ingredient_id)
            VALUES (?,?) 
            """,
            (int(id[0]),int(ingredient))
        )

# Actualizar tabla para incluir el número de ingredientes de la receta
for recipe in recipes:
    cursor.execute(
        f"""
        SELECT id FROM Recipes WHERE name = '{recipe['Name']}';
        """
    )
    id = cursor.fetchall()[0][0]
    cursor.execute(
        f"""
        SELECT COUNT(*) FROM RecipeIngredient WHERE recipe_id = {id}
        """
    )

    numberofingredients = cursor.fetchall()[0][0]

    cursor.execute(
        f"""
        UPDATE recipes
        SET numberofingredients = {numberofingredients}
        WHERE id = {id};
        """
    )

# Cierre de la conexión
conn.commit()
cursor.close()
conn.close()