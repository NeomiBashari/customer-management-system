import yaml
import mysql.connector
from mysql.connector import Error

class DatabaseConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._instance.connection = cls._create_connection()
        return cls._instance

    @staticmethod
    def _load_settings():
        with open("settings.yaml", "r") as settings_file:
            settings = yaml.safe_load(settings_file)
        with open("secrets.yaml", "r") as secrets_file:
            secrets = yaml.safe_load(secrets_file)
        return settings["database"], secrets["database_password"]

    @classmethod
    def _create_connection(cls):
        try:
            db_settings, db_password = cls._load_settings()
            conn = mysql.connector.connect(
                host=db_settings["host"],
                user=db_settings["user"],
                password=db_password,
                database=db_settings["database"]
            )
            print("Database connection established")
            return conn
        except Error as e:
            print(f"Error connecting to the database: {e}")
            raise

    def get_connection(self):
        return self.connection
    
class UserDAO:
    def __init__(self):
        self.db = DatabaseConnection().get_connection()

    def insert_user(self, email: str, password_hash: str, salt: str) -> int:
        try:
            cursor = self.db.cursor()
            cursor.execute(
                "INSERT INTO users (email, password_hash, salt) VALUES (%s, %s, %s)",
                (email, password_hash, salt)
            )
            self.db.commit()
            return cursor.lastrowid
        except Error as e:
            print(f"MySQL Error: {e}")
            raise
        finally:
            if cursor:
                cursor.close()

    def get_user_by_email(self, email: str) -> dict:
        try:
            cursor = self.db.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            return cursor.fetchone()
        except Error as e:
            print(f"MySQL Error: {e}")
            raise
        finally:
            if cursor:
                cursor.close()

    def update_user_password(self, email: str, password_hash: str, salt: str) -> None:
        try:
            cursor = self.db.cursor()
            cursor.execute(
                "UPDATE users SET password_hash = %s, salt = %s WHERE email = %s",
                (password_hash, salt, email)
            )
            self.db.commit()
        except Error as e:
            print(f"MySQL Error: {e}")
            raise
        finally:
            if cursor:
                cursor.close()