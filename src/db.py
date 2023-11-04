from sqlalchemy import create_engine, select, func, distinct
from sqlalchemy.orm import scoped_session, sessionmaker
from models import RecipeIngredient, Recipes, Ingredient
from decouple import config
import warnings

class Error_DB(Exception):
    pass

warnings.filterwarnings('ignore')

class Db_connector:
    """
    Clase para desacoplar la base de datos
    """
        
    def __init__(self,db : str, host : str = "", user : str = "", password : str = ""):
        """
        Constructor de clase

        Parameters
        ----------
        host : str
            Dirección de la base de datos.
        db : str
            Nombre de la base de datos.
        user : str
            Usuario de la base de datos.
        password : str
            Contraseña de la base de datos

        Raises
        ------

        Error_DB : Error en la conexión a la base de datos.
        """
        try:
            if not host and not user and not password:
                self._engine = create_engine(f"sqlite:///{db}?charset=utf8")
        except:
            raise Error_DB("Error de base de datos: Conexión fallida")
        
        if self._engine:
            self._session = scoped_session(sessionmaker(bind=self._engine))

    def buscar(self,query : str):
        """
        Método para ejecutar querys en la base de datos

        Parameters
        ----------

        query : str
            Solicitud a realizar

        Raises
        ------

        Error_DB : Fallo al ejecutar la sentencia
        Error_DB : No hay conexión con la base de datos
        """
        if self._session:
            try:            
                return self._session.query(query)
            except:
                Error_DB("Error de base de datos: Fallo al ejecutar la sentencia")
        else:
            raise Error_DB("Error de base de datos: No hay conexión con la base de datos")
        
    def buscarIngredienteNombre(self,name: str):
        if self._session:
            try:
                # Create the query
                query = select(Ingredient).where(Ingredient.name.like('%{}%'.format(name)))

                # Execute the query and get the results
                results = self._session.execute(query).all()
                format_results = []
                for result in results:
                    format_results.append((result[0].id,result[0].name))
                return format_results
            except:
                raise Error_DB("Error de base de datos: No hay conexión con la base de datos")
            
    def buscarIngredienteID(self,id: int):
        if self._session:
            try:
                # Create the query
                query = select(Ingredient).where(Ingredient.id == id)
                results = self._session.execute(query).one()
                return [(results[0].id,results[0].name)]
            except:
                raise Error_DB("Error de base de datos: No hay conexión con la base de datos")
    
    def getIngredientes(self, id: int):
        
        if self._session:
            try:
                # Create the query
                query = select(Ingredient.name).join(RecipeIngredient, RecipeIngredient.ingredient_id == Ingredient.id).filter(RecipeIngredient.recipe_id == id)
                results = self._session.execute(query).all()
                return results
            except:
                raise Error_DB("Error de base de datos: No hay conexión con la base de datos")
            
    def buscarRecetasNombre(self, name : str):
        try:
            query = select(Recipes.id,Recipes.name).where(Recipes.name.like('%{}%'.format(name)))
            return self._session.execute(query).all()
        except:
            raise Error_DB("Error de base de datos: No hay conexión con la base de datos")

    def buscarRecetasID(self, id: int):
        try:
            query = select(Recipes).where(Recipes.id == id)
            result = self._session.execute(query).first()
            return (result[0].id,result[0].name,result[0].steps,result[0].numberofingredients)
        except:
            raise Error_DB("Error de base de datos: No hay conexión con la base de datos")
        
    def buscarRecetasIngredientesNumber(self, id: list[int]):
        try:
            subquery = select(RecipeIngredient.recipe_id, func.count(RecipeIngredient.ingredient_id).label('numberofingredients')).group_by(RecipeIngredient.recipe_id)
            query = select(distinct(RecipeIngredient.recipe_id), Recipes.name).join(Recipes, Recipes.id == RecipeIngredient.recipe_id).filter(subquery.subquery().c.numberofingredients <= len(id)).where(RecipeIngredient.ingredient_id.in_(id))
            return self._session.execute(query).all()
        except:
            raise Error_DB("Error de base de datos: No hay conexión con la base de datos")
        
    def buscarRecetasIngredientes(self, id: int):
        try:
            query = select(RecipeIngredient.ingredient_id, Ingredient.name).join(RecipeIngredient, RecipeIngredient.ingredient_id == Ingredient.id).where(RecipeIngredient.recipe_id == id)
            return self._session.execute(query).all()
        except:
            raise Error_DB("Error de base de datos: No hay conexión con la base de datos")
        
    def getRecetasRandom(self, number: int):
        try:
            query = select(Recipes.id, Recipes.name).order_by(func.random()).limit(number)
            return self._session.execute(query).all()
        except:
            raise Error_DB("Error de base de datos: No hay conexión con la base de datos")
        
