# Simulation and Protection Guide - Cyber Project

This document outlines the project's compliance with requirements, how to simulate the specified attacks (XSS and SQLi), and the implemented protections.

## Project Requirements Checklist

### Part A: Secure Development

| Requirement         | Status         | Implementation Details                                                        |
| ------------------- | -------------- | ----------------------------------------------------------------------------- |
| **Relational DB**   | ✅ Implemented | MySQL (via Docker or Local)                                                   |
| **Web Platform**    | ✅ Implemented | React (Frontend) + Python FastAPI (Backend)                                   |
| **Register Screen** | ✅ Implemented | `create_user_with_validation`                                                 |
| **Password Logic**  | ✅ Implemented | HMAC + Salt (SHA256) in `UserController`                                      |
| **Config File**     | ✅ Implemented | `settings.yaml` (Policy: len 10, complexity, etc.)                            |
| **Login Screen**    | ✅ Implemented | `login` endpoint                                                              |
| **System Screen**   | ✅ Implemented | Customer Management (Add/View Customers)                                      |
| **Forgot Password** | ⚠️ Partial     | Implemented "Reset via Temp Password" flow. Spec asks for "SHA-1 Token" flow. |

### Part B: Vulnerabilities & Protections

| Requirement         | Status         | Notes                                                                                                            |
| ------------------- | -------------- | ---------------------------------------------------------------------------------------------------------------- |
| **Stored XSS**      | ✅ Simulated   | `CustomerManagement.vulnerable.tsx` demonstrates the attack.                                                     |
| **SQL Injection**   | ✅ Simulated   | `UserDAO` has a `get_user_by_email_vulnerable` method used by the unvalidated login endpoint.                    |
| **XSS Protection**  | ✅ Implemented | `bleach` sanitization in backend + React default escaping.                                                       |
| **SQLi Protection** | ✅ Implemented | Parameterized queries in `UserDAO` and `CustomerDAO`.                                                            |

---

## Part B: Attack Simulation & Protection

### 1. Stored XSS (Cross-Site Scripting)

**Description**:
Stored XSS occurs when an application receives data from an untrusted source and includes that data within its later HTTP responses in an unsafe way.

**Simulation (The Attack)**:

1.  **Navigate** to the "Customer Management (Vulnerable)" page in the React App.
2.  **Locate** the "Add New Customer" form.
3.  **Input** the following malicious payload into the "First Name" field:
    ```html
    <img src=x onerror=alert('XSS Attack Successful!')>
    ```
4.  **Submit** the form.
5.  **Observe**: When the "All Customers" list updates, an alert box with the text "XSS Attack Successful!" should appear immediately. This confirms the script executed in the browser.

**Protection (The Fix)**:

- **Method 1: Input Sanitization (Backend)**
  - In `CustomerController`, we use the `bleach` library to strip dangerous tags _before_ saving to the database.
  - _Code_: `first_name = bleach.clean(cust_req.firstname, tags=[], ...)`
- **Method 2: Output Encoding (Frontend)**
  - React naturally escapes content rendered in `{}`.
  - _Vulnerable Code_: `<span dangerouslySetInnerHTML={{ __html: customer.firstname }} />`
  - _Secure Code_: `<span>{customer.firstname}</span>`

---

### 2. SQL Injection (SQLi)

**Description**:
SQL Injection involves interfering with the queries an application makes to its database. It allows an attacker to bypass authentication or access unauthorized data by injecting malicious SQL code.

**Simulation (The Attack)**:

1.  **Vulnerable Scenario**: Login Bypass via Unvalidated Endpoint.
2.  **Target**: Login Page -> Switch to **"🔓 Unvalidated"** mode using the toggle button.
3.  **Input**:
    - **Email**: `admin@example.com' OR '1'='1' #`
    - **Password**: `anything`
4.  **How it works**:
    - The vulnerable backend uses string concatenation:
      ```python
      query = f"SELECT * FROM users WHERE email = '{email}'"
      ```
    - When you input `admin@example.com' OR '1'='1' #`, the query becomes:
      ```sql
      SELECT * FROM users WHERE email = 'admin@example.com' OR '1'='1' #'
      ```
    - The `'` closes the email string.
    - `OR '1'='1'` is a condition that is always true.
    - `#` comments out the trailing `'` so the query is valid.
    - The database returns the first user (usually the admin), bypassing the password check (because the vulnerable code skips password verification when SQL injection succeeds).

**Protection (The Fix)**:

The project protects against this implementation using **Parameterized Queries**.

- **Vulnerable (String Concatenation)**:
  Used in `get_user_by_email_vulnerable` (Unvalidated Route):
  ```python
  # VULNERABLE
  query = f"SELECT * FROM users WHERE email = '{email}'"
  cursor.execute(query)
  ```

- **Secure (Parameterized Query)**:
  Used in `get_user_by_email` (Validated Route):
  ```python
  # SECURE: The database driver treats the inputs as data, not executable code.
  cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
  ```

## Recommendations for Final Submission

1.  **Fix Forgot Password**: Update `UserController` to store a SHA-1 token in `password_reset_tokens` table instead of setting a temp password immediately, to strictly match the requirements.
