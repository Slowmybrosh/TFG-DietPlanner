from decouple import config

class Configuration:
    """Clase configuración para modularizar el uso de la base de datos"""
    _instance = None

    def __new__(cls):
        """Método para asegurar el singleton"""
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Constructor de clase"""
        self._db_name = config("DB_NAME")
        self._data_recipes = config("DATA_RECIPES")
        self._data_ingredients = config("DATA_INGREDIENTS")
    
    @property
    def db_name(self):
        """Getter nombre base de datos"""
        return self._db_name

    @property
    def data_recipes(self):
        """Getter ruta al fichero de recetas"""
        return self._data_recipes
    
    @property
    def data_ingredients(self):
        """Getter ruta al fichero de ingredientes"""
        return self._data_ingredients

