import psycopg2, csv, dotenv, os, json

dotenv.load_dotenv()

# Conexión con la base de datos
conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    port=5432,
    database="dietplanner",
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
)

# Creación de las tablas
cursor = conn.cursor()
cursor.execute(
    """
    CREATE TABLE Ingredients (
        id integer PRIMARY KEY,
        ingredient varchar(255)
    );
    """
)

cursor.execute(
    """
    CREATE TABLE Recipes (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255),
        steps TEXT
    );
    """
)

cursor.execute(
    """
    CREATE TABLE RecipeIngredient (
        recipe_id INTEGER,
        ingredient_id INTEGER,
        FOREIGN KEY (recipe_id) REFERENCES Recipes(id),
        FOREIGN KEY (ingredient_id) REFERENCES Ingredients(id),
        PRIMARY KEY (recipe_id, ingredient_id)
    );
    """
)

conn.commit()

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
            VALUES (%s, %s);
            """,
            (id, ingredient),
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
        VALUES (%s,%s);
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
            VALUES (%s,%s) 
            """,
            (int(id[0]),int(ingredient))
        )

# Cierre de la conexión
conn.commit()
cursor.close()
conn.close()