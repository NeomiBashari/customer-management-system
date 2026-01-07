import hmac
import hashlib
import secrets
import yaml
from fastapi import HTTPException

from models.user import UserCreateRequest, UserCreateResponse
from dao.user_dao import UserDAO

class UserController:
    def __init__(self):
        self.dao = UserDAO()
        self.policy = self.load_password_policy()

    def load_password_policy(self) -> dict:
        with open("settings.yaml") as f:
            config = yaml.safe_load(f)
        return config.get("password_policy", {})

    def validate_password(self, password: str) -> bool:
        policy = self.policy
        categories = 0
        if len(password) < policy.get("min_length", 8):
            return False
        if any(c.isupper() for c in password):
            categories += 1
        if any(c.islower() for c in password):
            categories += 1
        if any(c.isdigit() for c in password):
            categories += 1
        if any(c in "!@#$%^&*()-_=+[]{}|;:,.<>?/" for c in password):
            categories += 1
        if categories < policy.get("min_categories", 3):
            return False
        return True

    def hash_password(self, password: str, salt: str) -> str:
        return hmac.new(salt.encode(), password.encode(), hashlib.sha256).hexdigest()

    def create_user_with_validation(self, user_req: UserCreateRequest) -> UserCreateResponse:
        if not self.validate_password(user_req.password):
            raise HTTPException(status_code=400, detail="Password does not meet policy requirements")

        salt = secrets.token_hex(16)
        password_hash = self.hash_password(user_req.password, salt)

        try:
            user_id = self.dao.insert_user(user_req.email, password_hash, salt)
        except Exception as e:
            raise HTTPException(status_code=500, detail="Internal server error")

        return UserCreateResponse(id=user_id, email=user_req.email, message="User created successfully")

    def create_user_without_validation(self, user_req: UserCreateRequest) -> UserCreateResponse:

        salt = secrets.token_hex(16)
        password_hash = self.hash_password(user_req.password, salt)

        try:
            user_id = self.dao.insert_user(user_req.email, password_hash, salt)
        except Exception as e:
            raise HTTPException(status_code=500, detail="Internal server error")

        return UserCreateResponse(id=user_id, email=user_req.email, message="User created successfully")

    def login(self, email: str, password: str) -> dict:
        try:
            user = self.dao.get_user_by_email(email)

            if not user:
                raise HTTPException(status_code=401, detail="Invalid email or password")

            hashed_password = self.hash_password(password, user["salt"])
            if hashed_password != user["password_hash"]:
                raise HTTPException(status_code=401, detail="Invalid email or password")

            return {"message": "Login successful"}
        except Exception as e:
            raise HTTPException(status_code=500, detail="Internal server error")

    def change_password_with_validation(self, email: str, old_password: str, new_password: str) -> dict:
        user = self.dao.get_user_by_email(email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        hashed_old_password = self.hash_password(old_password, user["salt"])
        if hashed_old_password != user["password_hash"]:
            raise HTTPException(status_code=401, detail="Old password is incorrect")

        if not self.validate_password(new_password):
            raise HTTPException(status_code=400, detail="New password does not meet policy requirements")

        salt = secrets.token_hex(16)
        password_hash = self.hash_password(new_password, salt)
        self.dao.update_user_password(email, password_hash, salt)

        return {"message": "Password changed successfully"}

    def change_password_without_validation(self, email: str, old_password: str, new_password: str) -> dict:
        user = self.dao.get_user_by_email(email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        hashed_old_password = self.hash_password(old_password, user["salt"])
        if hashed_old_password != user["password_hash"]:
            raise HTTPException(status_code=401, detail="Old password is incorrect")

        salt = secrets.token_hex(16)
        password_hash = self.hash_password(new_password, salt)
        self.dao.update_user_password(email, password_hash, salt)

        return {"message": "Password changed successfully"}
