import yaml
import mysql.connector
from mysql.connector import Error, pooling

class DatabaseConnection:
    _pools = {}

    @staticmethod
    def _load_settings(db_key):
        with open("settings.yaml", "r") as settings_file:
            settings = yaml.safe_load(settings_file)
        with open("secrets.yaml", "r") as secrets_file:
            secrets = yaml.safe_load(secrets_file)
        
        # database_customer uses db_key "database_customer"
        # user_dao uses db_key "database"
        return settings[db_key], secrets["database_password"]

    @classmethod
    def get_connection(cls, db_key="database"):
        if db_key not in cls._pools:
            db_settings, db_password = cls._load_settings(db_key)
            pool_name = f"{db_key}_pool"
            cls._pools[db_key] = pooling.MySQLConnectionPool(
                pool_name=pool_name,
                pool_size=10,
                host=db_settings["host"],
                user=db_settings["user"],
                port=3307,
                password=db_password,
                database=db_settings["database"]
            )
        return cls._pools[db_key].get_connection()
