from configuration import Configuration
from db import Db_connector
class Error_Buscador(Exception):
    pass

class Buscador:
    """
    Clase para buscar recetas e ingredientes en la base de datos.

    Attributes
    ----------
        instance : Buscador
            Objeto de la clase buscador que obliga a tener solo una instancia de esta clase.
    """
    _instance = None

    def __new__(cls):
        """
        Método para asegurar que solo existe una instancia de esta clase.
        """
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """
        Constructor de clase.
        """
        self._conf = Configuration()
        self._db = Db_connector(self._conf.db_name)

    def getIngredientes(self,id: int):
        """
        Método para obtener los ingredientes de una receta por ID

        Parameters
        ----------
        id : int
            Identificador de la receta

        Returns
        -------
        lita_ingredientes : list<str>
            Lista de nombres de ingredientes que lleva la receta
        """
        query = "SELECT i.name FROM ingredients i JOIN recipeingredient ri ON ri.ingredient_id = i.id WHERE ri.recipe_id="+str(id)
        nombres = self._db.buscar(query)
        lista_ingredientes = []
        for nombre in nombres:
            lista_ingredientes.append(nombre[0])
        return lista_ingredientes

    def buscarIngrediente_Nombre(self,nombre : str):
        """
        Método que busca un ingrediente por nombre en la base de datos.

        Parameters
        ----------

        nombre : str
            Nombre del ingrediente a buscar.

        Raises
        ------

        Error_Buscador : La sentencia está mal escrita.

        Returns
        -------

        resultados : List<(idIngrediente, Nombre, Tipo)>
            Lista de ingredientes encontrados
        """
        try: 
            query = "SELECT * FROM ingredients WHERE name LIKE '%" + nombre + "%'"
            return self._db.buscar(query)
        except:
            raise Error_Buscador("Error Buscador: La sentencia de buscar ingrediente por nombre no es correcta")

    
    def buscarIngrediente_ID(self,ID : int):
        """
        Método que busca un ingrediente por identificador en la base de datos.

        Parameters
        ----------

        ID : Int
            Identificador del ingrediente.

        Raises
        ------

            Error_Buscador : La sentencia está mal escrita.

        Returns
        -------

        resultados : List<(idIngrediente, Nombre, Tipo)>
            Lista de ingredientes encontrados
        """
        try:

            query = "SELECT * FROM ingredients WHERE id="+str(ID)
            return self._db.buscar(query)
        except:
            raise Error_Buscador("Error Buscador: La sentencia de buscar ingrediente por ID no es correcta")
    
    def buscarRecetas_Nombre(self, nombre : str):
        """
        Método que busca una receta por nombre en la base de datos.

        Parameters
        ----------

        Nombre : str
            Nombre de la receta.

        Raises
        ------

            Error_Buscador : La sentencia está mal escrita.

        Returns
        -------
            
        resultados : List<(idReceta, numero de ingredientes, nombre, pasos, calorias, carbohidratos, proteinas, grasas)>
            Lista de recetas encontrados
        """
        try:
            query = "SELECT id, name FROM recipes WHERE name LIKE '%"+nombre+"%'"
            recetas = self._db.buscar(query)
            resultados = []
            for receta in recetas:
                query = "SELECT i.name FROM ingredients i JOIN RecipeIngredient ri ON ri.ingredient_id = i.id WHERE ri.recipe_id="+str(receta[0])
                nombres = self._db.buscar(query)
                lista_ingredientes = []
                for nombre in nombres:
                    lista_ingredientes.append(nombre[0])
                temp = receta + (lista_ingredientes,)
                resultados.append(temp)
            return resultados
        except:
            raise Error_Buscador("Error Buscador: La sentencia de buscar receta por nombre no es correcta")
        
    
    def buscarRecetas_ID(self, ID : int):
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
            
        resultados : List<(idReceta, numero de ingredientes, nombre, ingredientes)>
            Lista de recetas encontrados
        """
        try:
            query = "SELECT * FROM recipes WHERE id="+str(ID)
            resultado = list(self._db.buscar(query))
            lista_ingredientes = self.getIngredientes(ID)
            resultado[0] += tuple([lista_ingredientes])
            return resultado
        except:
            raise Error_Buscador("Error Buscador: La sentencia de buscar receta por ID no es correcta")
    
    def buscarRecetas_ingredientes(self,IDs : list):
        """
        Método que busca una receta por nombre en la base de datos.

        Parameters
        ----------

        IDs : List<Int>
            Identificadores de ingredientes a utilizar.

        Raises
        ------

            Error_Buscador : La sentencia está mal escrita.

        Returns
        -------
            
        resultados : List((idReceta, nombre)
            Lista de recetas que cumplen la condición
        """
        try:
            query = "SELECT DISTINCT ri.recipe_id, r.name FROM RecipeIngredient ri JOIN recipes r ON r.id = ri.recipe_id WHERE numberofingredients<="+str(len(IDs))+" AND (ri.ingredient_id="
            if len(IDs) > 1:
                for i in range(0,len(IDs)):
                    if i < len(IDs)-1:
                        addIngrediente = " OR ri.ingredient_id="
                    else:
                        addIngrediente = ");"
                    query = query + str(IDs[i]) + addIngrediente
            elif len(IDs) == 1:
                query = query + str(IDs[0]) + ");"
            print(query)
            resultados =  self._db.buscar(query)
        except:
            raise Error_Buscador("Error Buscador: La sentencia de buscar recetas por id de ingredientes no es correcta")
        try:
            recetas = []
            if resultados:
                query = "SELECT ri.ingredient_id, i.name FROM recipeingredient ri JOIN ingredients i ON ri.ingredient_id = i.id WHERE recipe_id="
                for item in resultados:
                    cumple = True
                    lista_ingredientes = []
                    resultados = self._db.buscar(query+str(item[0]))
                    for resultado in resultados:
                        if not (resultado[0] in IDs):
                            cumple = False
                            break
                        lista_ingredientes.append(resultado[1])
                    if cumple:
                        temp = item + (lista_ingredientes,)
                        recetas.append(temp)
            return recetas
        except:
            raise Error_Buscador("Error Buscador: La sentencia de buscar ingredientes por id de la receta no es correcta")

    def getRandom(self,numero : int):
        """
        Método para obtener recetas aleatorias de la base de datos

        Parameters
        ----------

        numero : int
            Número de recetas a obtener

        Returns
        -------

        recetas : list<(id,nombre)>
        """
        query = "SELECT id, name FROM recipes ORDER BY RANDOM() LIMIT " + str(numero)
        return self._db.buscar(query)