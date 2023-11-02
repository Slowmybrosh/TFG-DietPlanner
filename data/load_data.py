import sqlite3, csv, json

# Conexión con la base de datos
conn = sqlite3.connect('dietplanner.sqlite3')

# Creación de las tablas
cursor = conn.cursor()

# Resetear tablas
# cursor.execute('DROP TABLE Ingredients')
# cursor.execute('DROP TABLE Recipes')
# cursor.execute('DROP TABLE RecipeIngredient')
# conn.commit()

cursor.execute(
    '''CREATE TABLE IF NOT EXISTS Ingredients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ingredient TEXT NOT NULL
    );''')

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS Recipes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(255),
        steps TEXT
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
            INSERT INTO Ingredients (id, ingredient)
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
        INSERT INTO Recipes (name,steps)
        VALUES (?,?);
        """,
        (name,steps)
    )

conn.commit()

cursor.execute(
    """
    SELECT id, name from recipes;
    """
)
recipes_db = cursor.fetchall()

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

# Cierre de la conexión
conn.commit()
cursor.close()
conn.close()