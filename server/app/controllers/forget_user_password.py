import hashlib
import hmac
import secrets
import smtplib
import yaml
import mysql.connector
from mysql.connector import Error
from fastapi import HTTPException
from datetime import datetime, timedelta
from email.message import EmailMessage

from models.forget_user_password import (
    ForgotPasswordRequest,
    ForgotPasswordResponse,
    ForgotPasswordVerifyRequest,
    ForgotPasswordVerifyResponse,
)
from controllers.user_controller import UserController
from dao.user_dao import UserDAO


class ForgotPasswordController:
    def __init__(self):
        self.email_cfg = self.load_email_settings()

    def load_email_settings(self) -> dict:

        cfg = {}
        try:
            with open("settings.yaml") as f:
                cfg = yaml.safe_load(f) or {}
        except Exception:
            cfg = {}

        email_cfg = cfg.get("email", {}) or {}
        import os
        email_cfg.setdefault("smtp_host", os.getenv("SMTP_HOST"))
        email_cfg.setdefault("smtp_port", int(os.getenv("SMTP_PORT", "0")) or None)
        email_cfg.setdefault("smtp_user", os.getenv("SMTP_USER"))
        email_cfg.setdefault("smtp_password", os.getenv("SMTP_PASSWORD"))
        email_cfg.setdefault("from_email", os.getenv("SMTP_FROM"))
        tls_env = os.getenv("SMTP_USE_TLS")
        if "use_tls" not in email_cfg and tls_env is not None:
            email_cfg["use_tls"] = tls_env.lower() in ("1", "true", "yes")

        return email_cfg

    def ensure_reset_table(self):
        """
        Creates a table to store reset codes (hashed), if it doesn't exist.
        """
        sql = """
        CREATE TABLE IF NOT EXISTS password_reset_codes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            code_hash VARCHAR(128) NOT NULL,
            expires_at DATETIME NOT NULL,
            used TINYINT(1) NOT NULL DEFAULT 0,
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            INDEX (user_id),
            INDEX (expires_at)
        )
        """
        conn = None
        cursor = None
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            cursor.execute(sql)
            conn.commit()
        except Error as e:
            print(f"MySQL Error: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
   
    def generate_sha1_number_code(self, user_id: int) -> str:
        """
        Generates a 6-digit numeric code derived from SHA-1.
        """
        raw = f"{user_id}:{secrets.token_hex(16)}:{datetime.utcnow().isoformat()}".encode()
        digest = hashlib.sha1(raw).hexdigest()  
        code_int = int(digest[:8], 16) % 1_000_000
        return f"{code_int:06d}"

     def hash_code_for_storage(self, code: str) -> str:
        reset_secret = self.email_cfg.get("reset_secret", "change-me")
        return self.user_controller.hash_password(code, reset_secret)

    def save_code(self, user_id: int, code_hash: str, expires_at: datetime):
        conn = None
        cursor = None
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO password_reset_codes (user_id, code_hash, expires_at, used) VALUES (%s, %s, %s, 0)",
                (user_id, code_hash, expires_at),
            )
            conn.commit()
        except Error as e:
            print(f"MySQL Error: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def send_email(self, to_email: str, subject: str, body: str) -> bool:
        cfg = self.email_cfg or {}
        host = cfg.get("smtp_host")
        port = cfg.get("smtp_port") or 0
        user = cfg.get("smtp_user")
        pwd = cfg.get("smtp_password")
        from_email = cfg.get("from_email") or user
        use_tls = cfg.get("use_tls", True)

        # If SMTP not configured, we won't crash your dev server; we print the body instead.
        if not host or not port or not from_email:
            print("SMTP not configured. Email content:")
            print(body)
            return False

        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = from_email
        msg["To"] = to_email
        msg.set_content(body)

        try:
            with smtplib.SMTP(host, port, timeout=15) as server:
                server.ehlo()
                if use_tls:
                    server.starttls()
                    server.ehlo()
                if user and pwd:
                    server.login(user, pwd)
                server.send_message(msg)
            return True
        except Exception as e:
            print(f"Email send error: {e}")
            return False

    def request_reset(self, body: ForgotPasswordRequest) -> ForgotPasswordResponse:
        self.ensure_reset_table()

        user_id = int(body.user_id)
        email = self.get_user_email(user_id)

        code = self.generate_sha1_number_code(user_id)  # numeric code derived from SHA-1
        code_hash = self.hash_code_for_storage(code)
        expires_at = datetime.utcnow() + timedelta(minutes=15)

        self.save_code(user_id, code_hash, expires_at)

        sent = self.send_email(
            to_email=email,
            subject="Password reset code",
            body=f"Your password reset code is: {code}\n\nThis code expires in 15 minutes.",
        )

        msg = "Reset code sent to email" if sent else "Reset code generated (SMTP not configured - check server logs)"
        return ForgotPasswordResponse(user_id=user_id, message=msg)

    def verify_reset_password(self, body: ForgotPasswordVerifyRequest) -> ForgotPasswordVerifyResponse:
        self.ensure_reset_table()

        user_id = int(body.user_id)
        code_hash = self.hash_code_for_storage(body.code)

        conn = None
        cursor = None
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor(dictionary=True)

            cursor.execute(
                """
                SELECT id, code_hash
                FROM password_reset_codes
                WHERE user_id=%s AND used=0 AND expires_at > NOW()
                ORDER BY id DESC
                LIMIT 1
                """,
                (user_id,),
            )
            row = cursor.fetchone()
            if not row:
                raise HTTPException(status_code=400, detail="Code not found or expired")

            if not hmac.compare_digest(row["code_hash"], code_hash):
                raise HTTPException(status_code=400, detail="Invalid code")

            cursor.execute("UPDATE password_reset_codes SET used=1 WHERE id=%s", (row["id"],))
            conn.commit()

           
            return ForgotPasswordVerifyResponse(
                user_id=user_id,
                verified=True,
                message="Code verified. You can now change your password.",
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