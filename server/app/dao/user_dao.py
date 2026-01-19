from .db_connection import DatabaseConnection

class UserDAO:
    def insert_user(self, email: str, password_hash: str, salt: str) -> int:
        db = None
        cursor = None
        try:
            db = DatabaseConnection.get_connection()
            cursor = db.cursor(buffered=True)
            cursor.execute(
                "INSERT INTO users (email, password_hash, salt) VALUES (%s, %s, %s)",
                (email, password_hash, salt)
            )
            db.commit()
            return cursor.lastrowid
        except Error as e:
            print(f"MySQL Error: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
            if db:
                db.close()

    def get_user_by_email(self, email: str) -> dict:
        db = None
        cursor = None
        try:
            db = DatabaseConnection.get_connection()
            cursor = db.cursor(dictionary=True, buffered=True)
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            return cursor.fetchone()
        except Error as e:
            print(f"MySQL Error: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
            if db:
                db.close()

    def update_user_password(self, email: str, password_hash: str, salt: str):
        db = None
        cursor = None
        try:
            db = DatabaseConnection.get_connection()
            cursor = db.cursor(buffered=True)
            cursor.execute(
                "UPDATE users SET password_hash = %s, salt = %s WHERE email = %s",
                (password_hash, salt, email)
            )
            db.commit()
        except Error as e:
            print(f"MySQL Error: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
            if db:
                db.close()

    def get_password_reset_token(self, token_hash: str) -> dict:
        db = None
        cursor = None
        try:
            db = DatabaseConnection.get_connection()
            cursor = db.cursor(dictionary=True, buffered=True)
            cursor.execute(
                """
                SELECT email
                FROM users WHERE password_hash = %s
                """,
                (token_hash,)
            )
            return cursor.fetchone()
        except Error as e:
            print(f"MySQL Error: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
            if db:
                db.close()

    def invalidate_password_reset_token(self, token_hash: str) -> None:
        db = None
        cursor = None
        try:
            db = DatabaseConnection.get_connection()
            cursor = db.cursor(buffered=True)
            cursor.execute(
                "UPDATE password_reset_tokens SET used = TRUE WHERE token_hash = %s",
                (token_hash,)
            )
            db.commit()
        except Error as e:
            print(f"MySQL Error: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
            if db:
                db.close()