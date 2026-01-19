from .db_connection import DatabaseConnection

class CustomerDAO:
    def insert_customer(self, firstname: str, lastname: str, email: str) -> int:
        db = None
        cursor = None
        try:
            db = DatabaseConnection.get_connection("database_customer")
            cursor = db.cursor(buffered=True)
            cursor.execute(
                "INSERT INTO customers (firstname, lastname, email) VALUES (%s, %s, %s)",
                (firstname, lastname, email)
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

    def get_customer_by_email(self, email: str) -> dict:
        db = None
        cursor = None
        try:
            db = DatabaseConnection.get_connection("database_customer")
            cursor = db.cursor(dictionary=True, buffered=True)
            cursor.execute("SELECT * FROM customers WHERE email = %s", (email,))
            return cursor.fetchone()
        except Error as e:
            print(f"MySQL Error: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
            if db:
                db.close()
    
    def get_customer_by_id(self, id: str) -> dict:
        db = None
        cursor = None
        try:
            db = DatabaseConnection.get_connection("database_customer")
            cursor = db.cursor(dictionary=True, buffered=True)
            cursor.execute("SELECT * FROM customers WHERE id = %s", (id,))
            return cursor.fetchone()
        except Error as e:
            print(f"MySQL Error: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
            if db:
                db.close()

    def get_all_customers(self) -> list:
        db = None
        cursor = None
        try:
            db = DatabaseConnection.get_connection("database_customer")
            cursor = db.cursor(dictionary=True, buffered=True)
            cursor.execute("SELECT * FROM customers")
            return cursor.fetchall()
        except Error as e:
            print(f"MySQL Error: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
            if db:
                db.close()

