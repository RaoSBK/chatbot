# MoneyMind X - System Architecture

This document details the software architecture, system boundaries, component diagrams, flow patterns, security mechanisms, and scalability strategies for **MoneyMind X**.

---

## 1. High-Level Architecture

MoneyMind X follows a modern decoupled **Client-Server Architecture** featuring an AI-augmented and analytical backend. The system comprises three primary layers:
1. **Presentation Layer (Frontend):** A responsive Next.js web application.
2. **Application & Processing Layer (Backend & AI):** A highly performant FastAPI REST server and Python ML models, integrated with the external Google Gemini API.
3. **Storage & Data Layer (Database):** A relational PostgreSQL database with transactional integrity constraints.

### High-Level Block Diagram

```
+-----------------------------------------------------------+
|                   Presentation Layer                      |
|            [ Next.js Web App (Tailwind CSS) ]             |
+-----------------------------------------------------------+
                              |
                     HTTPS / JSON API (JWT)
                              v
+-----------------------------------------------------------+
|               Application & Processing Layer              |
|                                                           |
|    +--------------------+       +--------------------+    |
|    |      FastAPI       |<----->|  Python ML Engine  |    |
|    |     REST API       |       | (Stress / Predict) |    |
|    +--------------------+       +--------------------+    |
+-----------------------------------------------------------+
          |             |                        |
          |             |                        |
          v             v                        v
  [ PostgreSQL ]   [ Redis Cache ]       [ Google Gemini API ]
  (Storage Layer)   (Rate Limits)            (AI Layer)
```

---

## 2. Component Diagram

The following diagram illustrates the detailed modular layout, internal communication channels, and dependencies of the system:

```
+---------------------------------------------------------------------------------+
|                                 CLIENT CLIENT                                   |
|                                                                                 |
|   +-----------------------+   +------------------------+   +----------------+   |
|   |   Next.js Router      |   |   Zustand Auth Store   |   | Tailwind Style |   |
|   +-----------+-----------+   +-----------+------------+   +----------------+   |
|               |                           |                                     |
|               v                           v                                     |
|   +----------------------------------------------------+                        |
|   |         Fetch API Client (Automatic JWT Headers)   |                        |
|   +---------------------------+------------------------+                        |
+-------------------------------|-------------------------------------------------+
                                |
                        HTTPS (REST JSON)
                                |
                                v
+---------------------------------------------------------------------------------+
|                                 API GATEWAY                                     |
|                        Nginx Reverse Proxy & SSL                                |
+----------------------------------|----------------------------------------------+
                                   |
                                   v
+---------------------------------------------------------------------------------+
|                                 BACKEND (FastAPI)                               |
|                                                                                 |
|   +-------------------------------------------------------------------------+   |
|   |  API Routers (auth, expenses, budgets, goals, recommendation, stress)   |   |
|   +---+------------------+-------------------+--------------------------+---+   |
|       |                  |                   |                          |       |
|       v                  v                   v                          v       |
|   +--------+         +--------+         +----------+               +--------+   |
|   |  JWT   |         | Pydantic|        | DB Repo  |               | SlowAPI|   |
|   | Auth   |         | Schemas|         | Pattern  |               | RateLim|   |
|   +--------+         +--------+         +----+-----+               +----+---+   |
|                                              |                          |       |
+----------------------------------------------|--------------------------|-------+
                                               |                          |
                    SQLAlchemy (AsyncPG)       |                          |
                                               v                          v
+---------------------+             +--------------------+      +-----------------+
|   AI INTERACTION    |             |  POSTGRESQL DB     |      |   REDIS CACHE   |
|                     |             |                    |      |                 |
|  +---------------+  |             |  +--------------+  |      |  - Rate Limits  |
|  | Gemini Client |  |             |  | User/Expense |  |      |  - User Session |
|  +-------+-------+  |             |  | Schemas      |  |      |    Metadata     |
|          |          |             |  +--------------+  |      +-----------------+
+----------|----------+             +--------------------+
           |
     Gemini API (HTTPS)
           |
           v
+---------------------+
| Google GenAI Engine |
+---------------------+
```

---

## 3. Frontend Responsibilities

The Next.js client is responsible for rendering the visual representation of MoneyMind X, enforcing client-side validations, and managing user state:

* **Single Page App Routing:** Utilizes Next.js App Router for server-side layout optimization and fast client-side transition cycles.
* **State Management:** Manages JWT storage (via secure HttpOnly Cookies where possible, and transient context variables) and state updates using Zustand/Redux.
* **Interceptors:** Centralized API client wrapper to inject headers (`Authorization: Bearer <token>`) and handle global error responses (e.g. redirecting to login on HTTP 401).
* **Responsive Visual Styling:** Built using Tailwind CSS to scale dynamically from mobile devices to desktop monitors.
* **Form & Payload Validation:** Uses client-side validation schemas (e.g., Zod) matching Pydantic requirements to flag invalid payloads before transmission, minimizing server overhead.

---

## 4. Backend Responsibilities

The FastAPI backend functions as the secure transaction handler and integration layer:

* **Request Lifecycle & Routing:** Resolves RESTful endpoints, handles CORS origins verification, and manages API endpoint versioning under `/v1/`.
* **Dynamic Validation:** Employs Pydantic schemas to validate structural, type, and range constraints of inbound JSON payloads.
* **Authentication & Role Authorization:** Inspects JWT tokens in incoming requests, decodes scopes, and queries corresponding user entities from PostgreSQL.
* **Rate Limiting:** Protects endpoints from DDoS/brute-force attacks via SlowAPI token-bucket limitations.
* **Async Database Session Handling:** Employs SQLAlchemy 2.0 AsyncSessions to facilitate non-blocking database queries.

---

## 5. Database Layer

MoneyMind X relies on a **PostgreSQL** relational database structured for consistency and referential integrity:

```
                  +-------------------+
                  |       users       |
                  +-------------------+
                  | PK  id (UUID)     |
                  |     email (Str)   |
                  |     password (Str)|
                  +-------------------+
                     |      |      |
         +-----------+      |      +-----------+
         |                  |                  |
         v                  v                  v
+-----------------+  +-----------------+  +-----------------+
|    expenses     |  |    budgets      |  |     goals       |
+-----------------+  +-----------------+  +-----------------+
| PK  expense_id  |  | PK  budget_id   |  | PK  goal_id     |
| FK  user_id     |  | FK  user_id     |  | FK  user_id     |
|     amount      |  |     category    |  |     goal_name   |
|     category    |  |     limit       |  |     target_amt  |
+-----------------+  +-----------------+  +-----------------+
```

* **Constraints & Indexes:** 
  - Unique composite index on `(user_id, category)` within the budgets schema to prevent duplicate definitions.
  - Foreign key cascading targets user deletion.
  - B-tree indexing on `user_id` across `expenses`, `budgets`, and `goals` to optimize filter queries.

---

## 6. AI Layer

The AI layer integrates **Google Gemini API** dynamically through prompt engineering and isolated helper services:

* **Educational Investment Assistant:** Bound by static prompt wrappers restricting output to educational personal finance terms. It explicitly refuses to provide stock calls, direct trading recommendations, or fiduciary advice.
* **Payload Sanitation:** Checks user inputs for malicious injection vectors (e.g. system instructions override prompts) before invoking Google GenAI APIs.
* **Session Memory Preservation:** Maintains light-weight session state via UUID keys in Redis, storing recent query context to feed into Gemini requests.

---

## 7. Authentication Flow

Authentication is executed via stateless JSON Web Tokens (JWT). The lifecycle is illustrated below:

```
[ Client UI ]                [ FastAPI Auth ]               [ PostgreSQL ]
      |                             |                             |
      | 1. POST /login (username)   |                             |
      |---------------------------->|                             |
      |                             | 2. Fetch User & Hash verify |
      |                             |---------------------------->|
      |                             |<----------------------------|
      |                             |                             |
      | 3. Access & Refresh Tokens  |                             |
      |<----------------------------|                             |
      |                             |                             |
      | -- Access token expires --  |                             |
      |                             |                             |
      | 4. POST /refresh            |                             |
      |---------------------------->|                             |
      |                             | 5. Verify refresh signature |
      |                             |    (If valid)               |
      | 6. New Access Token         |                             |
      |<----------------------------|                             |
```

* **Access Token:** Short-lived token (15-30 minutes) containing user UUID and scopes, validated statelessly by verifying its HMAC-SHA256 signature.
* **Refresh Token:** Long-lived token (7-30 days) stored in a secure HttpOnly database-logged cache, used to request fresh access tokens.

---

## 8. Data Flow

This chart shows how transactional and analytic flows propagate through MoneyMind X:

```
[ Next.js UI ]       [ FastAPI Router ]      [ Postgres ]      [ ML Engine ]
      |                      |                    |                 |
      |  1. POST /expense    |                    |                 |
      |--------------------->|                    |                 |
      |                      | 2. Save Expense    |                 |
      |                      |------------------->|                 |
      |                      |<-------------------|                 |
      |                      |                                      |
      |  3. POST /stress/assess                   |                 |
      |------------------------------------------------------------>|
      |                      |                    | 4. Read history |
      |                      |                    |<----------------|
      |                      |                    |                 |
      |                      |                    | 5. Process Score|
      |                      |                    |-----------------|
      |                      |                    |<- - - - - - - - |
      |                      |                                      |
      |  6. Return Stress Response                                  |
      |<------------------------------------------------------------|
```

---

## 9. API Communication Flow

Every endpoint interaction conforms to standard HTTP request/response patterns over SSL/TLS:

1. **Serialization:** Object schemas are mapped from models to JSON structures using Pydantic.
2. **Dynamic Aggregation:** The `GET /budgets` endpoint fetches budget configurations from the database and runs aggregate queries on `expenses` for the active billing cycle. It returns current spending and remaining allowance fields calculated dynamically.
3. **External Latency Decoupling:** AI Chat actions communicate asynchronously with the Gemini API to prevent API blockages.

---

## 10. Security Architecture

MoneyMind X implements a multi-tier defense strategy:

* **Encryption in Transit:** Strict Transport Security (HSTS) with HTTPS-only (TLS 1.3 preferred, TLS 1.2 minimum).
* **Database Security:** PostgreSQL parameters are bound to internal VPC subnets. Passwords are saved with custom salt factors using **bcrypt**.
* **JWT Integrity:** Token structures use HMAC-SHA256 signatures with secret rotation protocols.
* **CORS and Origin Filtering:** Web clients are restricted to whitelist subdomains configured inside environments.
* **SlowAPI Defense:** Prevents authentication credential attacks by limiting registration and logins to 10 requests/minute.

---

## 11. Deployment Architecture

Containerization and server layout overview:

```
                           +--------------------------+
                           |     Internet Traffic     |
                           +------------+-------------+
                                        |
                                      HTTPS
                                        v
                           +--------------------------+
                           |  Nginx Load Balancer     |
                           +------------+-------------+
                                        |
                 +----------------------+----------------------+
                 | Private VPC                                 |
                 v                                             v
    +--------------------------+                  +--------------------------+
    |  FastAPI Application 01  |                  |  FastAPI Application 02  |
    |  [ Docker Container ]    |                  |  [ Docker Container ]    |
    +------------+-------------+                  +------------+-------------+
                 |                                             |
                 +----------------------+----------------------+
                                        |
                                        v
                           +--------------------------+
                           |  PostgreSQL Database     |
                           |  (Primary / Write replica)|
                           +--------------------------+
```

* **Containerization:** All services (Next.js, FastAPI, ML scripts) are packaged as isolated Docker containers.
* **Replication:** Database deployments use standard primary/replica partitions to prevent write-bottlenecks during high traffic periods.

---

## 12. Scalability Considerations

* **Database Connection Pools:** Implements SQLAlchemy async pools (`QueuePool`) with strict connection thresholds to prevent connection exhaustion.
* **Caching Layer:** Integrates Redis to cache frequently read configurations (e.g. User settings, Personality DNA profiles) and to manage SlowAPI token buckets.
* **Stateless API Scale:** Since FastAPI servers do not store state locally, the application layer can scale horizontally behind a load balancer.
