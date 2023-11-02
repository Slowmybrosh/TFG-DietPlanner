from decouple import config
import os

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
        self._db_host = config("DB_HOST")
        self._db_name = config("DB_NAME")
        self._db_user = config("DB_USER")
        self._db_password = config("DB_PASSWORD")

    @property
    def db_host(self):
        """Getter host base de datos"""
        return self._db_host
    
    @property
    def db_name(self):
        """Getter nombre base de datos"""
        return self._db_name
    
    @property
    def db_user(self):
        """Getter user base de datos"""
        return self._db_user
    
    @property
    def db_password(self):
        """Getter password base de datos"""
        return self._db_password
