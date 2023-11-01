import sqlite3
class Error_DB(Exception):
    pass

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
                self._conn = sqlite3.connect(db)
        except:
            raise Error_DB("Error de base de datos: Conexión fallida")
        
        if self._conn:
            self._cursor = self._conn.cursor()

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
        if self._conn:
            try :
                self._cursor.execute(query)
                return self._cursor.fetchall()
            except:
                Error_DB("Error de base de datos: Fallo al ejecutar la sentencia")
        else:
            raise Error_DB("Error de base de datos: No hay conexión con la base de datos")