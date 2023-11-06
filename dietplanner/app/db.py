from app.models import Ingredients, RecipeIngredient, Recipes
from django.db.models import Q, F
import warnings,random

class Error_DB(Exception):
    pass

warnings.filterwarnings('ignore')

class Db_connector:
    """
    Clase para desacoplar la base de datos
    """
        
    def __init__(self):
        """
        Constructor de clase
        """
        
    def buscarIngredienteNombre(self,name: str):
            """
            Método que recupera una lista de ingredientes de la base de datos

            Parameters
            ----------
            name : str
                Nombre del ingrediente a buscar.

            Raises
            ------
            Error_DB : No hay conexión con la base de datos.

            Returns
            -------
            resultados : List<(id, name)>
                Lista de ingredientes encontrados
            """
            try:
                results = Ingredients.objects.filter(name__icontains=name).all()
                format_results = []
                for result in results:
                    format_results.append((result.id,result.name))
                return format_results
            except:
                raise Error_DB("Error de base de datos: No hay conexión con la base de datos")
            
    def buscarIngredienteID(self,id: int):
        """
        Método que busca un ingrediente por identificador en la base de datos.

        Parameters
        ----------
        id : Int
            Identificador del ingrediente.

        Raises
        ------
        Error_DB : No hay conexión con la base de datos.

        Returns
        -------
        results : Tuple(id, name)
            Ingrediente encontrado
        """
        try:
            results = Ingredients.objects.get(id=id)
            return (results.id,results.name)
        except:
            raise Error_DB("Error de base de datos: No hay conexión con la base de datos")
    
    def getIngredientes(self, id: int):
            """
            Método para obtener los ingredientes de una receta por ID

            Parameters
            ----------
            id : int
                Identificador de la receta

            Raises
            ------
            Error_DB : No hay conexión con la base de datos.

            Returns
            -------
            list_ingredients : list<str>
                Lista de nombres de ingredientes que lleva la receta
            """
            try:
                list_ingredients = Ingredients.objects.filter(recipeingredient__recipe_id=id).select_related('recipeingredient').values_list('name', flat=True)
                return list_ingredients
            except:
                raise Error_DB("Error de base de datos: No hay conexión con la base de datos")
            
    def buscarRecetasNombre(self, name : str):
        """
        Método que busca una lista de recetas por nombre en la base de datos.

        Parameters
        ----------
        name : str
            Nombre de la receta.

        Raises
        ------
        Error_DB : No hay conexión con la base de datos.

        Returns
        -------
        resultados : List<(Recipes)>
            Lista de recetas encontradas
        """
        try:
            return Recipes.objects.filter(name__icontains=name).all()
        except:
            raise Error_DB("Error de base de datos: No hay conexión con la base de datos")

    def buscarRecetasID(self, id: int):
        """
        Método que busca una receta por identificador en la base de datos.

        Parameters
        ----------

        ID : Int
            Identificador de la receta.

        Raises
        ------

            Error_Buscador : La sentencia está mal escrita.

        Returns
        -------
            
        resultados : Tuple(id,name,steps,number_of_ingredients)
            Lista de recetas encontradas
        """
        try:
            result = Recipes.objects.get(id=id)
            return (result.id,result.name,result.steps,result.number_of_ingredients)
        except:
            raise Error_DB("Error de base de datos: No hay conexión con la base de datos")
        
    def buscarRecetasIngredientesNumber(self, id: list[int]):
        """
        Método que busca una lista de recetas por numero de ingredientes y que contengan al menos un ingrediente de la lista en la base de datos.

        Parameters
        ----------
        id : List<Int>
            Identificadores de ingredientes a utilizar.

        Raises
        ------
        Error_DB : No hay conexión con la base de datos.

        Returns
        -------
            
        resultados : List<(Recipes)>
            Lista de recetas que cumplen la condición
        """
        try:
            recipes = Recipes.objects.filter(
                Q(number_of_ingredients__lte=len(id)) & Q(recipeingredient__ingredient_id__in=id)
            ).distinct()
            return recipes.all()
        except:
            raise Error_DB("Error de base de datos: No hay conexión con la base de datos")
        
    def buscarRecetasIngredientes(self, id: int):
        """
        Método que recupera los ingredientes de una receta por identificador.

        Parameters
        ----------
        id : Int
            Identificador de receta

        Raises
        ------
        Error_DB : No hay conexión con la base de datos.

        Returns
        -------
        resultados : List<(ingredient_id,ingredient_name)>
            Lista de recetas que cumplen la condición
        """
        try:
            receta_ingredientes = RecipeIngredient.objects.filter(recipe_id=id).values('ingredient_id', ingredient_name=F('ingredient_id__name'))
            resultado = []
            for receta in receta_ingredientes:
                resultado.append((receta['ingredient_id'],receta['ingredient_name']))
            return resultado
        except:
            raise Error_DB("Error de base de datos: No hay conexión con la base de datos")
        
    def getRecetasRandom(self, number: int):
        """
        Método para obtener recetas aleatorias de la base de datos

        Parameters
        ----------
        number : int
            Número de recetas a obtener

        Raises
        ------
        Error_DB : No hay conexión con la base de datos.

        Returns
        -------
        recetas : list<(Recipes)>
        """
        try:
            items = list(Recipes.objects.all())
            random_items = random.sample(items,number)
            return random_items
        except:
            raise Error_DB("Error de base de datos: No hay conexión con la base de datos")
        
