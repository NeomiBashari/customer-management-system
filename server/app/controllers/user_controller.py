import hmac
import hashlib
import secrets
import yaml
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from fastapi import HTTPException
from models.user import UserCreateRequest, UserCreateResponse, UserLoginRequest, UserChangePasswordRequest, ForgotPasswordRequest
from dao.user_dao import UserDAO

class UserController:
    def __init__(self):
        self.dao = UserDAO()
        self.policy = self.load_password_policy()
        self.email_config = self._load_email_config()

    def load_password_policy(self) -> dict:
        with open("settings.yaml") as f:
            config = yaml.safe_load(f)
        return config.get("password_policy", {})

    def _load_email_config(self) -> dict:
        try:
            with open("settings.yaml", "r") as f:
                settings = yaml.safe_load(f)
            with open("secrets.yaml", "r") as f:
                secrets_data = yaml.safe_load(f)
        except FileNotFoundError as e:
            return {}
        except yaml.YAMLError as e:
            return {}

        email_settings = settings.get("email_settings", {})
        email_settings["email_password"] = secrets_data.get("email_password") 
        return email_settings

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
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

    def login_vulnerable(self, email: str, password: str) -> dict:
        try:
            user = self.dao.get_user_by_email_vulnerable(email)

            if not user:
                raise HTTPException(status_code=401, detail="Invalid email or password")

            return {"message": "Login successful", "user": {"id": user.get("id"), "email": user.get("email")}}
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

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

    def _send_temporary_password_email(self, recipient_email: str, temporary_password: str) -> bool:
        smtp_host = self.email_config.get("smtp_host")
        smtp_port = self.email_config.get("smtp_port")
        sender_email = self.email_config.get("sender_email")
        email_password = self.email_config.get("email_password")

        if not all([smtp_host, smtp_port, sender_email, email_password]):
            return False

        subject = "Your Temporary Password"
        body = f"""
        Hello {recipient_email},

        You have requested a temporary password. Your temporary password is:

        {temporary_password}

        Please use this password to log in. You will be prompted to create a new password immediately after logging in.

        If you did not request a temporary password, please ignore this email and secure your account.

        Thanks,
        Your App Team
        """
        msg = MIMEText(body, 'plain', 'utf-8')
        msg['Subject'] = Header(subject, 'utf-8')
        msg['From'] = Header(sender_email, 'utf-8')
        msg['To'] = Header(recipient_email, 'utf-8')

        try:
            with smtplib.SMTP(smtp_host, smtp_port) as server:
                server.starttls()
                server.login(sender_email, email_password)
                server.sendmail(sender_email, recipient_email, msg.as_string())
            return True
        except Exception as e:
            return False

    def initiate_forgot_password_validated(self, email: str) -> dict:
        user = self.dao.get_user_by_email(email)
        if not user:
            return {"message": "If an account with that email exists, a temporary password has been sent."}

        temporary_password = secrets.token_urlsafe(16)
        new_salt = secrets.token_hex(16)
        temporary_password_hash = self.hash_password(temporary_password, new_salt)

        try:
            self.dao.update_user_password(user["email"], temporary_password_hash, new_salt)
            self._send_temporary_password_email(user["email"], temporary_password)
            return {"message": "If an account with that email exists, a temporary password has been sent."}
        except Exception as e:
            raise HTTPException(status_code=500, detail="Internal server error")
            
    def initiate_forgot_password_unvalidated(self, email: str) -> dict:
        user = self.dao.get_user_by_email(email)
        
        temporary_password = secrets.token_urlsafe(16)
        new_salt = secrets.token_hex(16)
        temporary_password_hash = self.hash_password(temporary_password, new_salt)

        try:
            if user:
                self.dao.update_user_password(email, temporary_password_hash, new_salt)
                self._send_temporary_password_email(email, temporary_password)

            return {"message": "If an account with that email exists, a temporary password has been sent."}
        except Exception as e:
            raise HTTPException(status_code=500, detail="Internal server error")

    def reset_password_validated(self, email: str, old_password: str, new_password: str) -> dict:
        return self.change_password_with_validation(email, old_password, new_password)

    def reset_password_unvalidated(self, email: str, old_password: str, new_password: str) -> dict:
        return self.change_password_without_validation(email, old_password, new_password)
