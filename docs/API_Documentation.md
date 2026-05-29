# MoneyMind X - REST API Documentation

Welcome to the **MoneyMind X REST API** documentation. MoneyMind X is a next-generation personal finance platform offering core tracking (expenses, budgets, goals) along with advanced financial psychology engines (Stress Score, Personality DNA), smart recommendations, wealth growth simulation, and AI-powered financial/investment assistants.

## Global Configurations

- **Base URL:** `https://api.moneymindx.com/v1`
- **Default Format:** All request and response payloads are in `application/json`.
- **Date Format:** ISO 8601 extended date formats (`YYYY-MM-DD`) and datetime formats (`YYYY-MM-DDTHH:MM:SSZ`) are used throughout.
- **Precision:** Financial values are handled as high-precision decimals represented as string/number values depending on JSON parser preferences.

---

## Authentication & Authorization

All protected endpoints require authentication using a **JSON Web Token (JWT)** in the HTTP header:

```http
Authorization: Bearer <your_jwt_access_token>
```

### Rate Limiting
To prevent abuse, the API uses rate limiting via **SlowAPI**. The limits are:
* **Authentication endpoints:** 10 requests per minute.
* **AI Chat & Investment Assistant:** 60 requests per minute.
* **Standard endpoints (Expenses, Budgets, Goals, etc.):** 100 requests per minute.

When a limit is exceeded, the server returns an **HTTP 429 Too Many Requests** response.

---

## Error Handling

### Standard Error Response (HTTP 400, 401, 403, 404, 429, 500)
```json
{
  "detail": "Detailed error message explaining the failure."
}
```

### Validation Error Response (HTTP 422 Unprocessable Entity)
When request inputs fail validation (handled automatically by FastAPI and Pydantic):
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "value is not a valid email address",
      "type": "value_error.email"
    }
  ]
}
```

---

## Table of Contents
1. [Authentication](#1-authentication)
2. [Expenses](#2-expenses)
3. [Budgets](#3-budgets)
4. [Goals](#4-goals)
5. [Recommendations](#5-recommendations)
6. [Alerts](#6-alerts)
7. [Stress Score](#7-stress-score)
8. [Personality DNA](#8-personality-dna)
9. [Wealth Simulator](#9-wealth-simulator)
10. [AI Chat Assistant](#10-ai-chat-assistant)

---

## 1. Authentication

Endpoints related to user registration, login, session token refresh, and logout.

### Register User
* **URL:** `/auth/register`
* **HTTP Method:** `POST`
* **Description:** Register a new user account with MoneyMind X.
* **Authentication Required:** No
* **Rate Limit:** 10/minute
* **Request Body:**
  ```json
  {
    "full_name": "John Doe",
    "email": "john.doe@example.com",
    "password": "strongpassword123"
  }
  ```
* **Validation Rules:**
  - `full_name`: Optional. String up to 255 characters.
  - `email`: Required. Must be a valid email format.
  - `password`: Required. String with a minimum length of 6 characters.
  - Extra fields are strictly forbidden.
* **Response Body (HTTP 201 Created):**
  ```json
  {
    "id": "a3b98c9d-82d1-4cb5-827c-65b3c41efb70",
    "full_name": "John Doe",
    "email": "john.doe@example.com",
    "created_at": "2026-05-29T22:20:51Z",
    "updated_at": "2026-05-29T22:20:51Z"
  }
  ```
* **Error Responses:**
  - **HTTP 400 Bad Request:** User with this email already exists.
    ```json
    { "detail": "Email already registered." }
    ```
  - **HTTP 422 Unprocessable Entity:** Invalid email format or password too short.

---

### Login User
* **URL:** `/auth/login`
* **HTTP Method:** `POST`
* **Description:** Authenticate user credentials and return access & refresh tokens.
* **Authentication Required:** No
* **Rate Limit:** 10/minute
* **Request Body:** Supports standard OAuth2 Password flow (`application/x-www-form-urlencoded`) and JSON body payloads containing:
  ```json
  {
    "email": "john.doe@example.com",
    "password": "strongpassword123"
  }
  ```
* **Validation Rules:**
  - `email`: Required. Valid email format.
  - `password`: Required. Minimum 6 characters.
* **Response Body (HTTP 200 OK):**
  ```json
  {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer"
  }
  ```
* **Error Responses:**
  - **HTTP 401 Unauthorized:** Invalid email or password.
    ```json
    { "detail": "Incorrect email or password." }
    ```

---

### Refresh Token
* **URL:** `/auth/refresh`
* **HTTP Method:** `POST`
* **Description:** Exchange a valid refresh token for a new access token.
* **Authentication Required:** No
* **Request Body:**
  ```json
  {
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
  ```
* **Response Body (HTTP 200 OK):**
  ```json
  {
    "access_token": "new_eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "new_refresh_eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer"
  }
  ```
* **Error Responses:**
  - **HTTP 401 Unauthorized:** Expired or malformed refresh token.
    ```json
    { "detail": "Invalid or expired refresh token." }
    ```

---

### Logout User
* **URL:** `/auth/logout`
* **HTTP Method:** `POST`
* **Description:** Blacklist the current refresh token and terminate the active session.
* **Authentication Required:** Yes
* **Request Body:** None
* **Response Body (HTTP 200 OK):**
  ```json
  {
    "message": "Logged out successfully."
  }
  ```
* **Error Responses:**
  - **HTTP 401 Unauthorized:** Invalid or missing Bearer token.

---

## 2. Expenses

Create, retrieve, update, and delete expense tracking entries.

### Create Expense
* **URL:** `/expenses`
* **HTTP Method:** `POST`
* **Description:** Record a new monetary expense.
* **Authentication Required:** Yes
* **Rate Limit:** 100/minute
* **Request Body:**
  ```json
  {
    "amount": 42.50,
    "category": "Food & Dining",
    "payment_method": "Credit Card",
    "description": "Lunch at restaurant",
    "transaction_date": "2026-05-29"
  }
  ```
* **Validation Rules:**
  - `amount`: Required. Decimal value strictly greater than 0 (`gt=0`).
  - `category`: Required. String length between 1 and 100 characters.
  - `payment_method`: Optional. String up to 255 characters.
  - `description`: Optional. String.
  - `transaction_date`: Required. Valid date in `YYYY-MM-DD` format.
* **Response Body (HTTP 201 Created):**
  ```json
  {
    "expense_id": "c7f96b2e-0bb4-4cf1-8fb2-19e4871de991",
    "user_id": "a3b98c9d-82d1-4cb5-827c-65b3c41efb70",
    "amount": "42.50",
    "category": "Food & Dining",
    "payment_method": "Credit Card",
    "description": "Lunch at restaurant",
    "transaction_date": "2026-05-29",
    "created_at": "2026-05-29T22:25:00Z",
    "updated_at": "2026-05-29T22:25:00Z"
  }
  ```

---

### List Expenses
* **URL:** `/expenses`
* **HTTP Method:** `GET`
* **Description:** Retrieve paginated and filtered expenses for the logged-in user.
* **Authentication Required:** Yes
* **Request Parameters:**
  - `skip` (query): Optional. Integer. Default: `0`, min: `0`.
  - `limit` (query): Optional. Integer. Default: `20`, range: `1` to `100`.
  - `category` (query): Optional. String. Filter by category.
  - `start_date` (query): Optional. Format `YYYY-MM-DD`. Include expenses starting this date.
  - `end_date` (query): Optional. Format `YYYY-MM-DD`. Include expenses up to this date.
* **Response Body (HTTP 200 OK):**
  ```json
  [
    {
      "expense_id": "c7f96b2e-0bb4-4cf1-8fb2-19e4871de991",
      "user_id": "a3b98c9d-82d1-4cb5-827c-65b3c41efb70",
      "amount": "42.50",
      "category": "Food & Dining",
      "payment_method": "Credit Card",
      "description": "Lunch at restaurant",
      "transaction_date": "2026-05-29",
      "created_at": "2026-05-29T22:25:00Z",
      "updated_at": "2026-05-29T22:25:00Z"
    }
  ]
  ```

---

### Get Expense by ID
* **URL:** `/expenses/{expense_id}`
* **HTTP Method:** `GET`
* **Description:** Retrieve detailed information of a single expense record.
* **Authentication Required:** Yes
* **Request Parameters:**
  - `expense_id` (path): Required. UUID format.
* **Response Body (HTTP 200 OK):**
  ```json
  {
    "expense_id": "c7f96b2e-0bb4-4cf1-8fb2-19e4871de991",
    "user_id": "a3b98c9d-82d1-4cb5-827c-65b3c41efb70",
    "amount": "42.50",
    "category": "Food & Dining",
    "payment_method": "Credit Card",
    "description": "Lunch at restaurant",
    "transaction_date": "2026-05-29",
    "created_at": "2026-05-29T22:25:00Z",
    "updated_at": "2026-05-29T22:25:00Z"
  }
  ```
* **Error Responses:**
  - **HTTP 404 Not Found:** Expense not found or does not belong to user.
    ```json
    { "detail": "Expense not found." }
    ```

---

### Update Expense
* **URL:** `/expenses/{expense_id}`
* **HTTP Method:** `PUT`
* **Description:** Modify fields of an existing expense entry.
* **Authentication Required:** Yes
* **Request Parameters:**
  - `expense_id` (path): Required. UUID format.
* **Request Body:** All fields are optional (partial update support):
  ```json
  {
    "amount": 48.00,
    "description": "Lunch at restaurant with client"
  }
  ```
* **Validation Rules:**
  - `amount`: Optional. Decimal > 0.
  - `category`: Optional. String 1-100 characters.
  - `payment_method`: Optional. String up to 255 characters.
  - `transaction_date`: Optional. YYYY-MM-DD.
* **Response Body (HTTP 200 OK):**
  ```json
  {
    "expense_id": "c7f96b2e-0bb4-4cf1-8fb2-19e4871de991",
    "user_id": "a3b98c9d-82d1-4cb5-827c-65b3c41efb70",
    "amount": "48.00",
    "category": "Food & Dining",
    "payment_method": "Credit Card",
    "description": "Lunch at restaurant with client",
    "transaction_date": "2026-05-29",
    "created_at": "2026-05-29T22:25:00Z",
    "updated_at": "2026-05-29T22:27:00Z"
  }
  ```

---

### Delete Expense
* **URL:** `/expenses/{expense_id}`
* **HTTP Method:** `DELETE`
* **Description:** Remove an expense entry permanently.
* **Authentication Required:** Yes
* **Request Parameters:**
  - `expense_id` (path): Required. UUID format.
* **Response Body (HTTP 200 OK):**
  ```json
  {
    "expense_id": "c7f96b2e-0bb4-4cf1-8fb2-19e4871de991",
    "user_id": "a3b98c9d-82d1-4cb5-827c-65b3c41efb70",
    "amount": "48.00",
    "category": "Food & Dining",
    "payment_method": "Credit Card",
    "description": "Lunch at restaurant with client",
    "transaction_date": "2026-05-29",
    "created_at": "2026-05-29T22:25:00Z",
    "updated_at": "2026-05-29T22:27:00Z"
  }
  ```

---

## 3. Budgets

Set monthly expenditure ceilings for different categories and monitor spending.

### Create Budget
* **URL:** `/budgets`
* **HTTP Method:** `POST`
* **Description:** Create a new monthly budget limit for a category.
* **Authentication Required:** Yes
* **Request Body:**
  ```json
  {
    "category": "Entertainment",
    "monthly_limit": 300.00
  }
  ```
* **Validation Rules:**
  - `category`: Required. String 1-100 characters. Unique per user.
  - `monthly_limit`: Required. Decimal > 0.
* **Response Body (HTTP 201 Created):**
  ```json
  {
    "budget_id": "d1c76f4e-2875-4089-a292-f04b121abdf9",
    "user_id": "a3b98c9d-82d1-4cb5-827c-65b3c41efb70",
    "category": "Entertainment",
    "monthly_limit": "300.00",
    "current_spending": "0.00",
    "remaining_amount": "300.00",
    "created_at": "2026-05-29T22:28:10Z",
    "updated_at": "2026-05-29T22:28:10Z"
  }
  ```
* **Error Responses:**
  - **HTTP 400 Bad Request:** Budget category already exists for this user.
    ```json
    { "detail": "Budget for this category already exists." }
    ```

---

### List Budgets
* **URL:** `/budgets`
* **HTTP Method:** `GET`
* **Description:** Retrieve all budgets for the authenticated user, complete with dynamic current spending totals and remaining bounds based on recorded expenses.
* **Authentication Required:** Yes
* **Request Parameters:**
  - `skip` (query): Optional. Integer. Default `0`.
  - `limit` (query): Optional. Integer. Default `20`.
* **Response Body (HTTP 200 OK):**
  ```json
  [
    {
      "budget_id": "d1c76f4e-2875-4089-a292-f04b121abdf9",
      "user_id": "a3b98c9d-82d1-4cb5-827c-65b3c41efb70",
      "category": "Entertainment",
      "monthly_limit": "300.00",
      "current_spending": "120.50",
      "remaining_amount": "179.50",
      "created_at": "2026-05-29T22:28:10Z",
      "updated_at": "2026-05-29T22:28:10Z"
    }
  ]
  ```

---

### Get Budget by ID
* **URL:** `/budgets/{budget_id}`
* **HTTP Method:** `GET`
* **Description:** Retrieve details of a specific budget category limit.
* **Authentication Required:** Yes
* **Request Parameters:**
  - `budget_id` (path): Required. UUID format.
* **Response Body (HTTP 200 OK):**
  ```json
  {
    "budget_id": "d1c76f4e-2875-4089-a292-f04b121abdf9",
    "user_id": "a3b98c9d-82d1-4cb5-827c-65b3c41efb70",
    "category": "Entertainment",
    "monthly_limit": "300.00",
    "current_spending": "120.50",
    "remaining_amount": "179.50",
    "created_at": "2026-05-29T22:28:10Z",
    "updated_at": "2026-05-29T22:28:10Z"
  }
  ```

---

### Update Budget
* **URL:** `/budgets/{budget_id}`
* **HTTP Method:** `PUT`
* **Description:** Update an existing budget's parameters.
* **Authentication Required:** Yes
* **Request Parameters:**
  - `budget_id` (path): Required. UUID format.
* **Request Body:** All fields optional:
  ```json
  {
    "monthly_limit": 400.00
  }
  ```
* **Response Body (HTTP 200 OK):**
  ```json
  {
    "budget_id": "d1c76f4e-2875-4089-a292-f04b121abdf9",
    "user_id": "a3b98c9d-82d1-4cb5-827c-65b3c41efb70",
    "category": "Entertainment",
    "monthly_limit": "400.00",
    "current_spending": "120.50",
    "remaining_amount": "279.50",
    "created_at": "2026-05-29T22:28:10Z",
    "updated_at": "2026-05-29T22:29:45Z"
  }
  ```

---

### Delete Budget
* **URL:** `/budgets/{budget_id}`
* **HTTP Method:** `DELETE`
* **Description:** Delete a budget limit, releasing the configuration.
* **Authentication Required:** Yes
* **Request Parameters:**
  - `budget_id` (path): Required. UUID format.
* **Response Body (HTTP 200 OK):**
  ```json
  {
    "budget_id": "d1c76f4e-2875-4089-a292-f04b121abdf9",
    "user_id": "a3b98c9d-82d1-4cb5-827c-65b3c41efb70",
    "category": "Entertainment",
    "monthly_limit": "400.00",
    "current_spending": "120.50",
    "remaining_amount": "279.50",
    "created_at": "2026-05-29T22:28:10Z",
    "updated_at": "2026-05-29T22:29:45Z"
  }
  ```

---

## 4. Goals

Set financial targets (e.g. house purchase, emergency fund) and track savings progress.

### Create Goal
* **URL:** `/goals`
* **HTTP Method:** `POST`
* **Description:** Create a new savings target goal.
* **Authentication Required:** Yes
* **Request Body:**
  ```json
  {
    "goal_name": "Emergency Fund",
    "target_amount": 10000.00,
    "saved_amount": 1500.00,
    "target_date": "2027-05-29"
  }
  ```
* **Validation Rules:**
  - `goal_name`: Required. String 1-255 characters.
  - `target_amount`: Required. Decimal > 0.
  - `saved_amount`: Optional. Decimal >= 0. Default: `0.00`.
  - `target_date`: Required. YYYY-MM-DD format (must be in the future).
* **Response Body (HTTP 201 Created):**
  ```json
  {
    "goal_id": "f8a96c1e-3cb5-4ea2-972d-c11a098efcc9",
    "user_id": "a3b98c9d-82d1-4cb5-827c-65b3c41efb70",
    "goal_name": "Emergency Fund",
    "target_amount": "10000.00",
    "saved_amount": "1500.00",
    "target_date": "2027-05-29",
    "progress_percentage": 15.0,
    "status": "active",
    "created_at": "2026-05-29T22:30:00Z",
    "updated_at": "2026-05-29T22:30:00Z"
  }
  ```

---

### List Goals
* **URL:** `/goals`
* **HTTP Method:** `GET`
* **Description:** Retrieve list of user's financial goals.
* **Authentication Required:** Yes
* **Request Parameters:**
  - `skip` (query): Optional. Integer. Default `0`.
  - `limit` (query): Optional. Integer. Default `20`.
  - `status` (query): Optional. String. Filter by status (`active`, `completed`, `failed`).
* **Response Body (HTTP 200 OK):**
  ```json
  [
    {
      "goal_id": "f8a96c1e-3cb5-4ea2-972d-c11a098efcc9",
      "user_id": "a3b98c9d-82d1-4cb5-827c-65b3c41efb70",
      "goal_name": "Emergency Fund",
      "target_amount": "10000.00",
      "saved_amount": "1500.00",
      "target_date": "2027-05-29",
      "progress_percentage": 15.0,
      "status": "active",
      "created_at": "2026-05-29T22:30:00Z",
      "updated_at": "2026-05-29T22:30:00Z"
    }
  ]
  ```

---

### Get Goal by ID
* **URL:** `/goals/{goal_id}`
* **HTTP Method:** `GET`
* **Description:** Fetch detailed stats of a specific goal.
* **Authentication Required:** Yes
* **Request Parameters:**
  - `goal_id` (path): Required. UUID format.
* **Response Body (HTTP 200 OK):**
  ```json
  {
    "goal_id": "f8a96c1e-3cb5-4ea2-972d-c11a098efcc9",
    "user_id": "a3b98c9d-82d1-4cb5-827c-65b3c41efb70",
    "goal_name": "Emergency Fund",
    "target_amount": "10000.00",
    "saved_amount": "1500.00",
    "target_date": "2027-05-29",
    "progress_percentage": 15.0,
    "status": "active",
    "created_at": "2026-05-29T22:30:00Z",
    "updated_at": "2026-05-29T22:30:00Z"
  }
  ```

---

### Update Goal
* **URL:** `/goals/{goal_id}`
* **HTTP Method:** `PUT`
* **Description:** Edit parameters or track savings progress.
* **Authentication Required:** Yes
* **Request Parameters:**
  - `goal_id` (path): Required. UUID format.
* **Request Body:** All fields optional:
  ```json
  {
    "saved_amount": 2000.00
  }
  ```
* **Response Body (HTTP 200 OK):**
  ```json
  {
    "goal_id": "f8a96c1e-3cb5-4ea2-972d-c11a098efcc9",
    "user_id": "a3b98c9d-82d1-4cb5-827c-65b3c41efb70",
    "goal_name": "Emergency Fund",
    "target_amount": "10000.00",
    "saved_amount": "2000.00",
    "target_date": "2027-05-29",
    "progress_percentage": 20.0,
    "status": "active",
    "created_at": "2026-05-29T22:30:00Z",
    "updated_at": "2026-05-29T22:31:05Z"
  }
  ```

---

### Delete Goal
* **URL:** `/goals/{goal_id}`
* **HTTP Method:** `DELETE`
* **Description:** Remove a goal.
* **Authentication Required:** Yes
* **Request Parameters:**
  - `goal_id` (path): Required. UUID.
* **Response Body (HTTP 200 OK):**
  ```json
  {
    "goal_id": "f8a96c1e-3cb5-4ea2-972d-c11a098efcc9",
    "message": "Goal successfully deleted."
  }
  ```

---

### Record Goal Deposit
* **URL:** `/goals/{goal_id}/deposit`
* **HTTP Method:** `POST`
* **Description:** Increment the saved amount towards a savings target.
* **Authentication Required:** Yes
* **Request Parameters:**
  - `goal_id` (path): Required. UUID format.
* **Request Body:**
  ```json
  {
    "amount": 500.00
  }
  ```
* **Validation Rules:**
  - `amount`: Required. Decimal > 0.
* **Response Body (HTTP 200 OK):**
  ```json
  {
    "goal_id": "f8a96c1e-3cb5-4ea2-972d-c11a098efcc9",
    "user_id": "a3b98c9d-82d1-4cb5-827c-65b3c41efb70",
    "goal_name": "Emergency Fund",
    "target_amount": "10000.00",
    "saved_amount": "2500.00",
    "target_date": "2027-05-29",
    "progress_percentage": 25.0,
    "status": "active",
    "created_at": "2026-05-29T22:30:00Z",
    "updated_at": "2026-05-29T22:32:15Z"
  }
  ```

---

## 5. Recommendations

Smart analysis of user spending patterns and dynamic advisory triggers.

### Generate Savings Recommendations (Dynamic)
* **URL:** `/recommendations`
* **HTTP Method:** `POST`
* **Description:** Analyze an arbitrary financial payload (income and detailed expenses) to retrieve dynamic AI-generated recommendation rules without affecting stored database records.
* **Authentication Required:** No
* **Request Body:**
  ```json
  {
    "monthly_income": 5000.00,
    "expenses": [
      {
        "amount": 450.00,
        "category": "Dining Out",
        "date": "2026-05-01",
        "description": "Weekly dining bills"
      },
      {
        "amount": 150.00,
        "category": "Subscriptions",
        "date": "2026-05-15",
        "description": "Streaming apps"
      }
    ]
  }
  ```
* **Validation Rules:**
  - `monthly_income`: Required. Decimal > 0.
  - `expenses`: Required. Non-empty array of expense objects:
    - `amount`: Required. Decimal > 0.
    - `category`: Required. String 1-100 characters.
    - `date`: Required. YYYY-MM-DD format.
    - `description`: Optional. String.
* **Response Body (HTTP 200 OK):**
  ```json
  [
    {
      "recommendation_type": "Dining Out Spending",
      "severity": "Medium",
      "possible_savings": 150.00,
      "confidence": 0.85,
      "recommendation": "Reduce weekly dining budget from $450 to $300.",
      "reason": "Dining Out accounts for 9% of your monthly income. Shifting 30% of this budget to grocery cooking saves $150/month."
    },
    {
      "recommendation_type": "Subscriptions",
      "severity": "Low",
      "possible_savings": 50.00,
      "confidence": 0.9,
      "recommendation": "Consolidate unused media streaming plans.",
      "reason": "Multiple similar streaming subscriptions are active. Cancelling duplicates saves $50/month."
    }
  ]
  ```

---

### Fetch Stored Recommendations
* **URL:** `/recommendations`
* **HTTP Method:** `GET`
* **Description:** Retrieve system-generated recommendations tailored to the active user's historical db data.
* **Authentication Required:** Yes
* **Response Body (HTTP 200 OK):**
  ```json
  [
    {
      "recommendation_id": "e2f78b1d-c50f-48d6-a2e1-4560d23fb456",
      "recommendation_type": "Subscription Audit",
      "severity": "Low",
      "possible_savings": "25.00",
      "confidence": 0.95,
      "recommendation": "Cancel under-utilized Gym Membership.",
      "reason": "No logs matching recreation or wellness expenses were recorded in the last 60 days.",
      "status": "active",
      "created_at": "2026-05-29T22:00:00Z"
    }
  ]
  ```

---

### Update Recommendation Status
* **URL:** `/recommendations/{recommendation_id}/status`
* **HTTP Method:** `PUT`
* **Description:** Mark a recommendation as accepted, dismissed, or applied.
* **Authentication Required:** Yes
* **Request Parameters:**
  - `recommendation_id` (path): Required. UUID.
* **Request Body:**
  ```json
  {
    "status": "applied"
  }
  ```
* **Validation Rules:**
  - `status`: Required. Must be one of `active`, `accepted`, `dismissed`, `applied`.
* **Response Body (HTTP 200 OK):**
  ```json
  {
    "recommendation_id": "e2f78b1d-c50f-48d6-a2e1-4560d23fb456",
    "status": "applied",
    "updated_at": "2026-05-29T22:35:10Z"
  }
  ```

---

## 6. Alerts

System and budget trigger notifications.

### Retrieve Alerts
* **URL:** `/alerts`
* **HTTP Method:** `GET`
* **Description:** Retrieve notifications, threshold warnings, and milestones for the logged-in user.
* **Authentication Required:** Yes
* **Request Parameters:**
  - `unread_only` (query): Optional. Boolean. Default `false`.
  - `type` (query): Optional. String. Filter by type (`budget_warning`, `goal_milestone`, `system`).
* **Response Body (HTTP 200 OK):**
  ```json
  [
    {
      "alert_id": "a9a8c7b6-c5e4-4d3c-b2a1-0f9e8d7c6b5a",
      "user_id": "a3b98c9d-82d1-4cb5-827c-65b3c41efb70",
      "type": "budget_warning",
      "title": "Budget Threshold Warning",
      "message": "You have spent 85% of your 'Entertainment' budget.",
      "is_read": false,
      "created_at": "2026-05-29T22:15:30Z"
    }
  ]
  ```

---

### Mark Alert as Read
* **URL:** `/alerts/{alert_id}/read`
* **HTTP Method:** `PUT`
* **Description:** Mark an alert notification as read.
* **Authentication Required:** Yes
* **Request Parameters:**
  - `alert_id` (path): Required. UUID.
* **Response Body (HTTP 200 OK):**
  ```json
  {
    "alert_id": "a9a8c7b6-c5e4-4d3c-b2a1-0f9e8d7c6b5a",
    "is_read": true,
    "updated_at": "2026-05-29T22:36:00Z"
  }
  ```

---

### Mark All Alerts Read
* **URL:** `/alerts/read-all`
* **HTTP Method:** `POST`
* **Description:** Mark all active notifications for the user as read.
* **Authentication Required:** Yes
* **Response Body (HTTP 200 OK):**
  ```json
  {
    "message": "All alerts successfully marked as read.",
    "marked_count": 3
  }
  ```

---

### Dismiss Alert
* **URL:** `/alerts/{alert_id}`
* **HTTP Method:** `DELETE`
* **Description:** Remove/dismiss an alert.
* **Authentication Required:** Yes
* **Request Parameters:**
  - `alert_id` (path): Required. UUID.
* **Response Body (HTTP 200 OK):**
  ```json
  {
    "alert_id": "a9a8c7b6-c5e4-4d3c-b2a1-0f9e8d7c6b5a",
    "message": "Alert successfully dismissed."
  }
  ```

---

## 7. Stress Score

Calculates a financial health/mental wellness score based on spending habits, volatility, and reserves.

### Assess Stress Score
* **URL:** `/stress/assess`
* **HTTP Method:** `POST`
* **Description:** Run a financial stress evaluation score (0-100) using current system assets, expenses, savings rate, and debts. Returns detailed contributing factor segments and actionable mitigation steps.
* **Authentication Required:** Yes
* **Request Body:**
  ```json
  {
    "monthly_debt_payments": 500.00,
    "dependents_count": 2,
    "has_stable_income": true
  }
  ```
* **Validation Rules:**
  - `monthly_debt_payments`: Required. Decimal >= 0.
  - `dependents_count`: Optional. Integer >= 0. Default `0`.
  - `has_stable_income`: Required. Boolean.
* **Response Body (HTTP 200 OK):**
  ```json
  {
    "stress_score": 38.5,
    "stress_category": "Moderate",
    "factors": {
      "debt_to_income_ratio": 0.1,
      "emergency_fund_months_coverage": 1.5,
      "savings_rate_percentage": 12.0,
      "spending_volatility_coefficient": 0.22
    },
    "action_steps": [
      "Increase emergency fund to cover at least 3 months of expenses.",
      "Review subscriptions to boost savings rate from 12% to 15%.",
      "Maintain debt-to-income ratio below 15%."
    ],
    "assessed_at": "2026-05-29T22:38:15Z"
  }
  ```

---

### Fetch Stress Score History
* **URL:** `/stress/history`
* **HTTP Method:** `GET`
* **Description:** Retrieve historical stress assessments to track financial stress patterns over time.
* **Authentication Required:** Yes
* **Response Body (HTTP 200 OK):**
  ```json
  [
    {
      "assessment_id": "b1b2c3d4-e5f6-4a5b-6c7d-8e9f0a1b2c3d",
      "stress_score": 42.0,
      "stress_category": "Moderate",
      "assessed_at": "2026-04-29T10:00:00Z"
    },
    {
      "assessment_id": "c1d2e3f4-a5b6-7c8d-9e0f-1a2b3c4d5e6f",
      "stress_score": 38.5,
      "stress_category": "Moderate",
      "assessed_at": "2026-05-29T22:38:15Z"
    }
  ]
  ```

---

## 8. Personality DNA

Assess and identify the user's spending archetype and cognitive biases regarding wealth.

### Assess Personality DNA
* **URL:** `/personality/assess`
* **HTTP Method:** `POST`
* **Description:** Submit answers to the Money Mindset questionnaire (usually 10 multiple-choice questions) to compute the user's Money Personality DNA archetype.
* **Authentication Required:** Yes
* **Request Body:**
  ```json
  {
    "answers": [
      { "question_id": "q1", "selected_option_id": "opt_c" },
      { "question_id": "q2", "selected_option_id": "opt_a" },
      { "question_id": "q3", "selected_option_id": "opt_b" }
    ]
  }
  ```
* **Validation Rules:**
  - `answers`: Required. Non-empty array of answer configurations:
    - `question_id`: Required. String.
    - `selected_option_id`: Required. String.
* **Response Body (HTTP 200 OK):**
  ```json
  {
    "personality_type": "Strategic Builder",
    "description": "You balance short-term enjoyment with long-term compound growth. You evaluate large purchases logically but occasionally experience friction when investing in volatile assets.",
    "traits": {
      "strengths": ["Consistent budget adherence", "Analytical risk assessment"],
      "weaknesses": ["Analysis paralysis in volatile markets", "Over-frugal anxiety"]
    },
    "investment_style": "Growth-oriented diversified index funds with minor value-tilt bias.",
    "compatibility_tips": "Pair with automated savings systems to bypass purchase anxiety.",
    "assessed_at": "2026-05-29T22:40:00Z"
  }
  ```

---

### Fetch Personality Profile
* **URL:** `/personality`
* **HTTP Method:** `GET`
* **Description:** Retrieve the active user's calculated financial Personality DNA archetype.
* **Authentication Required:** Yes
* **Response Body (HTTP 200 OK):**
  ```json
  {
    "personality_type": "Strategic Builder",
    "description": "You balance short-term enjoyment with long-term compound growth. You evaluate purchases logically but occasionally experience friction when investing.",
    "traits": {
      "strengths": ["Consistent budget adherence", "Analytical risk assessment"],
      "weaknesses": ["Analysis paralysis in volatile markets", "Over-frugal anxiety"]
    },
    "investment_style": "Growth-oriented diversified index funds with minor value-tilt bias.",
    "compatibility_tips": "Pair with automated savings systems to bypass purchase anxiety.",
    "assessed_at": "2026-05-29T22:40:00Z"
  }
  ```
* **Error Responses:**
  - **HTTP 404 Not Found:** User has not yet taken the assessment.
    ```json
    { "detail": "Money Personality DNA assessment not found. Please complete the assessment first." }
    ```

---

## 9. Wealth Simulator

Execute compound growth and Monte Carlo projection runs to evaluate target milestones.

### Run Wealth Simulation
* **URL:** `/simulator/run`
* **HTTP Method:** `POST`
* **Description:** Run a multi-scenario compound growth simulation based on net worth, monthly savings contributions, expected yield, and inflation factors.
* **Authentication Required:** Yes
* **Request Body:**
  ```json
  {
    "initial_net_worth": 15000.00,
    "monthly_contribution": 500.00,
    "annual_return_rate": 8.0,
    "investment_horizon_years": 15,
    "inflation_rate": 2.5
  }
  ```
* **Validation Rules:**
  - `initial_net_worth`: Required. Decimal >= 0.
  - `monthly_contribution`: Required. Decimal >= 0.
  - `annual_return_rate`: Required. Float between -10.0 and 30.0.
  - `investment_horizon_years`: Required. Integer between 1 and 50.
  - `inflation_rate`: Optional. Float between 0.0 and 15.0. Default `2.0`.
* **Response Body (HTTP 200 OK):**
  ```json
  {
    "inputs": {
      "initial_net_worth": "15000.00",
      "monthly_contribution": "500.00",
      "real_annual_return_rate": 5.5,
      "investment_horizon_years": 15
    },
    "summary": {
      "total_contributions": "90000.00",
      "total_interest_earned": "62432.18",
      "ending_net_worth_nominal": "252542.40",
      "ending_net_worth_real": "167432.18"
    },
    "yearly_projections": [
      {
        "year": 1,
        "nominal_value": "22340.50",
        "real_value": "21790.80"
      },
      {
        "year": 5,
        "nominal_value": "59410.20",
        "real_value": "53120.40"
      },
      {
        "year": 10,
        "nominal_value": "132540.80",
        "real_value": "104190.10"
      },
      {
        "year": 15,
        "nominal_value": "252542.40",
        "real_value": "167432.18"
      }
    ]
  }
  ```

---

## 10. AI Chat Assistant

Interact with the MoneyMind X general finance chat interface and the dedicated educational investment assistant.

### General Financial Chat
* **URL:** `/chat`
* **HTTP Method:** `POST`
* **Description:** Interact with the MoneyMind X conversational financial assistant. The assistant can view context like user's expenses/budgets if requested.
* **Authentication Required:** Yes
* **Rate Limit:** 60/minute
* **Request Body:**
  ```json
  {
    "message": "Can you summarize my spending category breakdown for last week?",
    "session_id": "chat-session-3b7c"
  }
  ```
* **Validation Rules:**
  - `message`: Required. String with a minimum length of 1 character.
  - `session_id`: Optional. String. Used to map thread memory.
* **Response Body (HTTP 200 OK):**
  ```json
  {
    "session_id": "chat-session-3b7c",
    "reply": "Certainly! Last week, your primary spending category was 'Food & Dining' (accounting for 65% of your $200 weekly total), followed by 'Transportation' (18%) and 'Entertainment' (17%).",
    "context_used": true,
    "timestamp": "2026-05-29T22:45:10Z"
  }
  ```

---

### Educational Investment Assistant Chat
* **URL:** `/investment-assistant/chat`
* **HTTP Method:** `POST`
* **Description:** Query the specialized educational AI Investment Assistant to learn about investment vehicles, concepts, and asset classes. This assistant is strictly educational and does not provide active investment advice.
* **Authentication Required:** Yes
* **Rate Limit:** 60/minute
* **Request Body:**
  ```json
  {
    "message": "What is the difference between an index fund and a mutual fund?",
    "session_id": "investment-session-2a1c"
  }
  ```
* **Validation Rules:**
  - `message`: Required. String (1+ characters).
  - `session_id`: Optional. String.
* **Response Body (HTTP 200 OK):**
  ```json
  {
    "session_id": "investment-session-2a1c",
    "topic": "Index Funds vs. Mutual Funds",
    "response": "An index fund is a type of mutual fund that tracks a specific market index (e.g., S&P 500) passively, leading to lower management fees. A standard mutual fund is typically actively managed by a portfolio manager aiming to beat market indices, which results in higher expense ratios. Generally, passive index funds outperform most actively managed mutual funds over long horizons.",
    "timestamp": "2026-05-29T22:46:00Z"
  }
  ```
