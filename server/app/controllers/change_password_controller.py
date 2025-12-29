import hmac
import hashlib
import secrets
import yaml
import mysql.connector
from mysql.connector import Error
from fastapi import HTTPException

from models.change_password import ChangePasswordRequest, ChangePasswordResponse


class ChangePasswordController:
    def __init__(self):
        self.policy = self.load_password_policy()

    def load_password_policy(self) -> dict:
        with open("settings.yaml") as f:
            config = yaml.safe_load(f) or {}
        return config.get("password_policy", {}) or {}

    def validate_password(self, password: str) -> bool:
        """
        Validates password according to settings.yaml -> password_policy.
        Uses the same rules as your UserController, plus optional min_categories if exists.
        """
        policy = self.policy

        if len(password) < policy.get("min_length", 8):
            return False

        categories = 0

        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        special_set = "!@#$%^&*()-_=+[]{}|;:,.<>?/"
        has_special = any(c in special_set for c in password)

        if has_upper:
            categories += 1
        if has_lower:
            categories += 1
        if has_digit:
            categories += 1
        if has_special:
            categories += 1

        if policy.get("require_uppercase") and not has_upper:
            return False
        if policy.get("require_lowercase") and not has_lower:
            return False
        if policy.get("require_digit") and not has_digit:
            return False
        if policy.get("require_special") and not has_special:
            return False

        min_categories = policy.get("min_categories")
        if isinstance(min_categories, int) and min_categories > 0:
            if categories < min_categories:
                return False

        return True

    def hash_password(self, password: str, salt: str) -> str:
        # Same hashing style as your UserController
        return hmac.new(salt.encode(), password.encode(), hashlib.sha256).hexdigest()

    def get_db_connection(self):
        return mysql.connector.connect(
            host="127.0.0.1",
            user="myuser",
            password="mypassword",
            database="user_data",
        )

    def change_password(self, body: ChangePasswordRequest) -> ChangePasswordResponse:
        user_id = int(body.user_id)

        conn = None
        cursor = None

        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()

            # 1) Find user salt + password_hash
            cursor.execute(
                "SELECT password_hash, salt FROM users WHERE id=%s LIMIT 1",
                (user_id,),
            )
            row = cursor.fetchone()
            if not row:
                raise HTTPException(status_code=404, detail="User not found")

            stored_hash, salt = row[0], row[1]

            # 2) Validate current password matches the DB (user_id + password match)
            current_hash = self.hash_password(body.current_password, salt)
            if not hmac.compare_digest(current_hash, stored_hash):
                raise HTTPException(status_code=401, detail="Current password is incorrect")

            # 3) Validate new password by policy
            if not self.validate_password(body.new_password):
                raise HTTPException(status_code=400, detail="New password does not meet policy requirements")

            # 4) Update password with new salt + new hash
            new_salt = secrets.token_hex(16)
            new_hash = self.hash_password(body.new_password, new_salt)

            cursor.execute(
                "UPDATE users SET password_hash=%s, salt=%s WHERE id=%s",
                (new_hash, new_salt, user_id),
            )
            conn.commit()

            return ChangePasswordResponse(
                user_id=user_id,
                message="Password changed successfully",
            )

        except HTTPException:
            raise
        except Error as e:
            print(f"MySQL Error: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
