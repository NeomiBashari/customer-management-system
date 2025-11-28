import hmac
import hashlib
import secrets
import yaml
import mysql.connector
from mysql.connector import Error
from fastapi import HTTPException

from models.user import UserCreateRequest, UserCreateResponse


class UserController:
    def __init__(self):
        self.policy = self.load_password_policy()

    def load_password_policy(self) -> dict:
        with open("settings.yaml") as f:
            config = yaml.safe_load(f)
        return config.get("password_policy", {})

    def validate_password(self, password: str) -> bool:
        policy = self.policy
        if len(password) < policy.get("min_length", 8):
            return False
        if policy.get("require_uppercase") and not any(c.isupper() for c in password):
            return False
        if policy.get("require_lowercase") and not any(c.islower() for c in password):
            return False
        if policy.get("require_digit") and not any(c.isdigit() for c in password):
            return False
        if policy.get("require_special") and not any(c in "!@#$%^&*()-_=+[]{}|;:,.<>?/" for c in password):
            return False
        return True

    def hash_password(self, password: str, salt: str) -> str:
        return hmac.new(salt.encode(), password.encode(), hashlib.sha256).hexdigest()

    def get_db_connection(self):
        return mysql.connector.connect(
            host="127.0.0.1",
            user="myuser",
            password="mypassword",
            database="user_data"
        )

    def create_user(self, user_req: UserCreateRequest) -> UserCreateResponse:
        if not self.validate_password(user_req.password):
            raise HTTPException(status_code=400, detail="Password does not meet policy requirements")
        
        salt = secrets.token_hex(16)
        password_hash = self.hash_password(user_req.password, salt)

        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (email, password_hash, salt) VALUES (%s, %s, %s)",
                (user_req.email, password_hash, salt)
            )
            conn.commit()
            user_id = cursor.lastrowid
        except Error as e:
            print(f"MySQL Error: {e}") 
            raise HTTPException(status_code=500, detail="Internal server error")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

        return UserCreateResponse(id=user_id, email=user_req.email, message="User created successfully")
