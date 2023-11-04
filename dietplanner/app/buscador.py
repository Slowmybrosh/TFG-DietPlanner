from .configuration import Configuration
from .db import Db_connector
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
        self._db = Db_connector()

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
        nombres = self._db.getIngredientes(id)
        lista_ingredientes = []
        for nombre in nombres:
            lista_ingredientes.append(nombre)
        return lista_ingredientes

    def buscarIngredienteNombre(self,nombre : str):
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

        resultados : List<(idIngrediente, Nombre>
            Lista de ingredientes encontrados
        """
        try: 
            return self._db.buscarIngredienteNombre(nombre)
        except:
            raise Error_Buscador("Error Buscador: La sentencia de buscar ingrediente por nombre no es correcta")

    
    def buscarIngredienteID(self,ID : int):
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

        resultados : List<(idIngrediente, Nombre)>
            Lista de ingredientes encontrados
        """
        try:
            return self._db.buscarIngredienteID(ID)
        except:
            raise Error_Buscador("Error Buscador: La sentencia de buscar ingrediente por ID no es correcta")
    
    def buscarRecetasNombre(self, nombre : str):
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
            recetas = self._db.buscarRecetasNombre(nombre)
            resultados = []
            for receta in recetas:
                nombres = self._db.getIngredientes(receta.id)
                lista_ingredientes = []
                for nombre in nombres:
                    lista_ingredientes.append(nombre)
                resultados.append((receta.id,receta.name,lista_ingredientes))
            return resultados
        except:
            raise Error_Buscador("Error Buscador: La sentencia de buscar receta por nombre no es correcta")
        
    
    def buscarRecetasID(self, ID : int):
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
            resultado = self._db.buscarRecetasID(ID)
            lista_ingredientes = self.getIngredientes(ID)
            return [(resultado[0],resultado[1],resultado[2],resultado[3],lista_ingredientes)]
        except:
            raise Error_Buscador("Error Buscador: La sentencia de buscar receta por ID no es correcta")
    
    def buscarRecetasIngredientes(self,IDs : list):
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
            resultados =  self._db.buscarRecetasIngredientesNumber(IDs)
        except:
            raise Error_Buscador("Error Buscador: La sentencia de buscar recetas por id de ingredientes no es correcta")
        try:
            recetas = []
            if resultados:
                for item in resultados:
                    cumple = True
                    lista_ingredientes = []
                    resultados = self._db.buscarRecetasIngredientes(item.id)
                    for resultado in resultados:
                        if not (resultado[0] in IDs):
                            cumple = False
                            break
                        lista_ingredientes.append(resultado[1])
                    if cumple:
                        recetas.append((item.id,item.name,lista_ingredientes))
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
        return self._db.getRecetasRandom(numero)