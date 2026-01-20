# E-commerce REST API - Implementation Documentation

---

## 🏗️ Project Setup

### 1. Clone the repository
```sh
git clone <(https://github.com/madihanazir/ecommerce-api.git)>
cd <ECOM_API>
```

### 2. Create a virtual environment
```sh
python -m venv venv
```

### 3. Activate the virtual environment
- **Windows:**
  ```sh
  venv\Scripts\activate
  ```
- **macOS/Linux:**
  ```sh
  source venv/bin/activate
  ```

### 4. Install dependencies
```sh
pip install -r requirements.txt
```
### 5. Make database migrations
```sh
python manage.py makemigrations
```

### 6. Apply database migrations
```sh
python manage.py migrate
```

### 7. Start the development server
```sh
python manage.py runserver
```

---

## 🧪 Comprehensive Testing Report

### 📊 Test Suite Overview
- **Total Tests:** 6 `pytest` cases covering critical functionality
- **Test Coverage:** Authentication, CRUD operations, atomic transactions
- **Test Execution:**  
  ```sh
  pytest tests/ -v
  ```
  All tests passing

---

### 🔐 Authentication Testing

#### ✅ JWT Login/Register Testing

- **Test 1: Successful JWT Login**  
  `POST /api/v1/auth/login/`

- **Test 2: User Registration**  
  `POST /api/v1/auth/register/`

#### ✅ Protected Endpoint Testing

- **Test 3: Access Profile with Valid Token**  
  `GET /api/v1/users/me/`  
  **Headers:**  
  `Authorization: Bearer <jwt-token>`  
  **Response:**  
  `200 OK` with user data

- **Test 4: Access Without Token**  
  `GET /api/v1/users/me/`  
  **Response:**  
  `401 Unauthorized` (correct error format)

---

### 🔍 Error Handling Implementation

- **401 Unauthorized Handling**
  ```json
  {
    "success": false,
    "data": null,
    "error": {
      "code": "UNAUTHORIZED",
      "message": "Authentication credentials were not provided.",
      "details": null
    },
    "meta": {
      "timestamp": 1764747264.8654747,
      "status_code": 401
    }
  }
  ```

- **403 Forbidden Handling (RBAC)**
  ```json
  {
    "success": false,
    "data": null,
    "error": {
      "code": "FORBIDDEN",
      "message": "You do not have permission to perform this action.",
      "details": null
    },
    "meta": {
      "timestamp": 1764747725.7980735,
      "status_code": 403
    }
  }
  ```

- **404 Not Found Handling**
  ```json
  {
    "success": false,
    "data": null,
    "error": {
      "code": "NOT_FOUND",
      "message": "No CartItem matches the given query.",
      "details": null
    },
    "meta": {
      "timestamp": 1764747822.6822324,
      "status_code": 404
    }
  }
  ```

---

### 🎯 Idempotency Implementation 

#### ✅ Idempotency-Key Requirement

- **Order creation (`POST /api/v1/orders/create/`) must include:**
  - `Authorization: Bearer <token>`
  - `Idempotency-Key: <required>`
  - `Content-Type: application/json`

**Without Idempotency-Key:**
- Response: `400 Bad Request` (error: "idempotency-key header required")

#### ✅ Idempotency Proof Workflow

**Test Case:** Preventing duplicate orders  
1. **First Request (New Order):**
    - Headers:
      ```yaml
      Authorization: Bearer <token>
      Idempotency-Key: unique-order-123
      ```
    - Body:
      ```json
      {"shipping_address": "123 Main St"}
      ```
    - Response:  
      `201 Created`  
      Order ID: `b9a73beb-a84e-4f13-98c9-e4038d1c8111`

2. **Second Request (Same Idempotency-Key):**
    - Same headers and body as above
    - Response:  
      `200 OK`  
      Returns: SAME Order ID: `b9a73beb-a84e-4f13-98c9-e4038d1c8111`

**Result:**  
No duplicate order created; same response returned, ensuring idempotency.

---

### ⚡ Atomic Transaction Implementation 

#### ✅ Atomic Order Creation Proof

**Test Data:**
- Product: "table" (ID: `c64f1987-0aff-43b6-b16f-8f8a048d5334`)
- Stock: 8 units  
- Order Quantity: 1 unit

**Transaction Timeline:**

1. **Before Order Creation:**
    ```json
    {
      "product": { "stock": 8 },
      "quantity": 1
    }
    ```

2. **Order Creation Request:**  
   `POST /api/v1/orders/create/`  
   `Idempotency-Key: test-atomic-123`  
   Result: Stock decrement, order created

3. **After Order Creation:**
    ```json
    {
      "items": [
        {
          "product": { "stock": 7 },
          "quantity": 1
        }
      ]
    }
    ```

- **Stock Before:** 8
- **Stock After:** 7
- **Decrement:** 1 (matches order quantity)
- **Time Difference:** 42 seconds
- **Transaction:** Stock decrement and order creation occur atomically

---

## 🏆 Key Requirements Met

| Requirement                 | Status       | Proof                                       |
|-----------------------------|--------------|----------------------------------------------|
| Atomic Order Creation       | ✅ FULLY MET | Stock decrement 8→7, single transaction     |
| Idempotency Support         | ✅ FULLY MET | Idempotency-Key required, duplicate prevention|
| Standardized Response Format| ✅ FULLY MET | {success, data, error, meta}                |
| JWT Authentication          | ✅ FULLY MET | Login/Register/Refresh/Profile OK           |
| 401/403/404 Error Handling  | ✅ FULLY MET | Correct codes & format                      |
| RBAC Implementation         | ✅ PARTIALLY | Admin/user permissions shown                |
| Cart System                 | ✅ PARTIALLY | Add/view works, update/delete untested      |
| Testing Coverage            | ✅ MET       | 6 passing tests                             |

---

## ⚠️ Untested Areas 

1. **Cart Item Update/Delete** – Needs specific item IDs  
2. **Product Update/Delete** – Limited testing due to token expiration  
3. **Order Status Updates** – Admin endpoint exists but untested  
4. **Concurrent Race Conditions** – Atomicity verified, concurrency untested  

---

## 📸 API Documentation (Swagger UI)

### 🔹 Swagger Overview
![Swagger UI](screenshots/swagger_main.png)

### 🔹 JWT Authorization Modal
![JWT Auth](screenshots/swagger_auth.png)
![JWT Auth](screenshots/swagger_auth2.png)
![JWT Auth](screenshots/swagger_auth3.png)

### 🔹 Categories Endpoint Response
![Categories](screenshots/swagger_categories.png)

---

> **Check at [`http://127.0.0.1:8000/docs/#/`](http://127.0.0.1:8000/docs/#/) after setting up the project**


---

## 🔐 Authentication & Security Module (New Features)

This module implements a secure, production-grade authentication pipeline with email verification, JWT authentication, role-based access control, and password recovery.

✅ Features Added

- Email Verification on Registration

  New users are created with:

  - `is_active = False`
  - `email_verified = False`

  A unique verification token is generated.

  Login is blocked until verification is complete.

- JWT Authentication with Custom Claims

  Access tokens include:

  - `user_id`
  - `email`
  - `role`

  Enables RBAC and downstream authorization.

- Login Blocking Until Email Verified

  Unverified users cannot obtain JWT tokens.

  Enforced centrally in the JWT serializer.

- Secure Password Reset Flow

  Time-limited, single-use reset tokens.

  Password confirmation enforced.

  Token invalidated after successful reset.

- Role-Based Access Control (RBAC)

  Custom permissions:

  - `IsAdmin`
  - `IsCustomer`

  Enforced on protected endpoints using JWT role claim.

🌐 Key Endpoints

| Purpose         | Method | Endpoint                                             |
|-----------------|--------|------------------------------------------------------|
| Register        | POST   | `/api/v1/auth/register/`                             |
| Verify Email    | GET/POST | `/api/v1/auth/verify-email/<uuid:token>/`          |
| Login (JWT)     | POST   | `/api/v1/auth/login/`                                |
| Refresh Token   | POST   | `/api/v1/auth/refresh/`                              |
| Logout          | POST   | `/api/v1/auth/logout/`                               |
| Forgot Password | POST   | `/api/v1/auth/password/forgot/`                      |
| Reset Password  | POST   | `/api/v1/auth/password/reset/<uuid:token>/`         |

🛡️ Security Guarantees

- Email ownership is enforced: no login without verification.

- No user enumeration: forgot password does not leak account existence.

- Token safety:

  - Email verification tokens are single-use and time-limited.

  - Password reset tokens are single-use and invalidated after success.

- Account activation control:

  - Only verified users are marked `is_active = True`.

- RBAC enforcement:

  - Role is embedded in JWT and enforced at view level.

🏗️ Architecture Notes

User lifecycle:

REGISTER
  ↓
is_active = False
email_verified = False
(token generated)
  ↓
VERIFY EMAIL
  ↓
is_active = True
email_verified = True
token cleared
  ↓
LOGIN ENABLED

Centralized enforcement:

Login restrictions are enforced in:

`CustomTokenObtainPairSerializer.validate()`

Ensures no alternate login path can bypass verification.

🧪 Evaluation Checklist

To validate this module:

- Register a new user → account inactive
- Attempt login → blocked
- Verify email → account activated
- Login → JWT issued with role claim
- Forgot password → token generated, no info leak
- Reset password → token invalidated
- Reuse token → blocked