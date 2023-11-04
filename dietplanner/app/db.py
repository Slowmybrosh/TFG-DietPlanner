from decouple import config
from app.models import Ingredients, RecipeIngredient, Recipes
from django.db.models import Q, Prefetch, OrderBy, F
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
            try:
                results = Ingredients.objects.filter(name__icontains=name).all()
                format_results = []
                for result in results:
                    format_results.append((result.id,result.name))
                return format_results
            except:
                raise Error_DB("Error de base de datos: No hay conexión con la base de datos")
            
    def buscarIngredienteID(self,id: int):
            try:
                # Create the query
                results = Ingredients.objects.get(id=id)
                return [(results.id,results.name)]
            except:
                raise Error_DB("Error de base de datos: No hay conexión con la base de datos")
    
    def getIngredientes(self, id: int):
            try:
                # Create the query
                results = Ingredients.objects.filter(recipeingredient__recipe_id=id).select_related('recipeingredient').values_list('name', flat=True)
                return results
            except:
                raise Error_DB("Error de base de datos: No hay conexión con la base de datos")
            
    def buscarRecetasNombre(self, name : str):
        try:
            return Recipes.objects.filter(name__icontains=name).all()
        except:
            raise Error_DB("Error de base de datos: No hay conexión con la base de datos")

    def buscarRecetasID(self, id: int):
        try:
            result = Recipes.objects.get(id=id)
            return (result.id,result.name,result.steps,result.number_of_ingredients)
        except:
            raise Error_DB("Error de base de datos: No hay conexión con la base de datos")
        
    def buscarRecetasIngredientesNumber(self, id: list[int]):
        try:
            recipes = Recipes.objects.filter(
                Q(number_of_ingredients__lte=len(id))
                & Q(recipeingredient__ingredient_id__in=id)
                ).distinct()
            return recipes.all()
        except:
            raise Error_DB("Error de base de datos: No hay conexión con la base de datos")
        
    def buscarRecetasIngredientes(self, id: int):
        try:
            receta_ingredientes = RecipeIngredient.objects.filter(recipe_id=id).values('ingredient_id', ingredient_name=F('ingredient_id__name'))
            resultado = []
            for receta in receta_ingredientes:
                resultado.append((receta['ingredient_id'],receta['ingredient_name']))
            return resultado
        except:
            raise Error_DB("Error de base de datos: No hay conexión con la base de datos")
        
    def getRecetasRandom(self, number: int):
        try:
            items = list(Recipes.objects.all())
            random_items = random.sample(items,number)
            return random_items
        except:
            raise Error_DB("Error de base de datos: No hay conexión con la base de datos")
        
