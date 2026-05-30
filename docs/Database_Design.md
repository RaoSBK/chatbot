# MoneyMind X - Database Design

This document details the relational database design for **MoneyMind X** using PostgreSQL. It describes the entities, schemas, indexing strategies, normalization forms, and query optimization guidelines.

---

## 1. Entity-Relationship (ER) Diagram

The diagram below details the table structures and relationships within the schema. Cardinality notations: `1` to `N` (one-to-many) and `1` to `1` (one-to-one).

```
  +-----------------------+
  |         users         |
  +-----------------------+
  | PK  id (UUID)         |
  |     email (VARCHAR)   |
  |     password (VARCHAR)|
  +-----------------------+
      |
      |----------------------------------------------------+
      | 1                                                  | 1
      | N                                                  | 1
      +---> [ expenses ] (1:N)                             +---> [ personality_profiles ] (1:1)
      |     PK: expense_id                                 |     PK: profile_id
      |     FK: user_id                                    |     FK: user_id
      |                                                    |
      +---> [ budgets ] (1:N)                              +---> [ stress_scores ] (1:N)
      |     PK: budget_id                                  |     PK: assessment_id
      |     FK: user_id                                    |     FK: user_id
      |                                                    |
      +---> [ goals ] (1:N)                                +---> [ chat_history ] (1:N)
      |     PK: goal_id                                    |     PK: message_id
      |     FK: user_id                                    |     FK: user_id
      |                                                    |
      +---> [ recommendations ] (1:N)                      +----------------------------------+
      |     PK: recommendation_id                          
      |     FK: user_id                                    
      |                                                    
      +---> [ alerts ] (1:N)                               
            PK: alert_id                                   
            FK: user_id                                    
```

---

## 2. Table Specifications

### 2.1 Users (`users`)
* **Purpose:** Stores the core onboarding, identity, and security credentials of registered platform users.
* **Fields:**
  - `id`: `UUID` (Primary Key). Unique identifier.
  - `full_name`: `VARCHAR(255)` (Nullable). Display name.
  - `email`: `VARCHAR(255)` (Not Null, Unique). Registration email.
  - `hashed_password`: `VARCHAR(255)` (Not Null). Secure bcrypt hash of credentials.
  - `created_at`: `TIMESTAMP WITH TIME ZONE` (Not Null). Default: `CURRENT_TIMESTAMP`.
  - `updated_at`: `TIMESTAMP WITH TIME ZONE` (Not Null). Default: `CURRENT_TIMESTAMP`.
* **Constraints:**
  - `PK_users`: Primary key constraint on `id`.
  - `UQ_users_email`: Unique constraint on `email`.
  - Check constraint enforcing non-empty string on `email` and `hashed_password`.
* **Relationships:**
  - Has zero-to-many (`1:N`) relationships with `expenses`, `budgets`, `goals`, `recommendations`, `alerts`, `stress_scores`, and `chat_history`.
  - Has a zero-to-one (`1:1`) relationship with `personality_profiles`.

---

### 2.2 Expenses (`expenses`)
* **Purpose:** Stores individual financial transaction records for users.
* **Fields:**
  - `expense_id`: `UUID` (Primary Key).
  - `user_id`: `UUID` (Not Null, Foreign Key).
  - `amount`: `NUMERIC(12, 2)` (Not Null). High-precision monetary transaction amount.
  - `category`: `VARCHAR(100)` (Not Null). Expense categorization.
  - `payment_method`: `VARCHAR(255)` (Nullable). Form of payment (e.g. Credit Card).
  - `description`: `TEXT` (Nullable). Extra notes.
  - `transaction_date`: `DATE` (Not Null). The calendar date of the expense.
  - `created_at`: `TIMESTAMP WITH TIME ZONE` (Not Null). Default: `CURRENT_TIMESTAMP`.
  - `updated_at`: `TIMESTAMP WITH TIME ZONE` (Not Null). Default: `CURRENT_TIMESTAMP`.
* **Constraints:**
  - `PK_expenses`: Primary key on `expense_id`.
  - `FK_expenses_users`: Foreign key `user_id` referencing `users.id` with `ON DELETE CASCADE`.
  - `CK_expenses_amount_positive`: Check constraint `amount > 0`.
* **Relationships:**
  - Belongs to a user (`N:1`).

---

### 2.3 Budgets (`budgets`)
* **Purpose:** Tracks monthly expense caps allocated for specific spend categories.
* **Fields:**
  - `budget_id`: `UUID` (Primary Key).
  - `user_id`: `UUID` (Not Null, Foreign Key).
  - `category`: `VARCHAR(100)` (Not Null). Targeted spending category.
  - `monthly_limit`: `NUMERIC(12, 2)` (Not Null). Budget limit.
  - `created_at`: `TIMESTAMP WITH TIME ZONE` (Not Null). Default: `CURRENT_TIMESTAMP`.
  - `updated_at`: `TIMESTAMP WITH TIME ZONE` (Not Null). Default: `CURRENT_TIMESTAMP`.
* **Constraints:**
  - `PK_budgets`: Primary key on `budget_id`.
  - `FK_budgets_users`: Foreign key `user_id` referencing `users.id` with `ON DELETE CASCADE`.
  - `UQ_budgets_user_category`: Composite unique index on `(user_id, category)` to prevent duplicate budgets for the same category.
  - `CK_budgets_limit_positive`: Check constraint `monthly_limit > 0`.
* **Relationships:**
  - Belongs to a user (`N:1`).

---

### 2.4 Goals (`goals`)
* **Purpose:** Manages financial targets (e.g. saving goals) and marks incremental progress.
* **Fields:**
  - `goal_id`: `UUID` (Primary Key).
  - `user_id`: `UUID` (Not Null, Foreign Key).
  - `goal_name`: `VARCHAR(255)` (Not Null). Goal title.
  - `target_amount`: `NUMERIC(12, 2)` (Not Null). Savings target.
  - `saved_amount`: `NUMERIC(12, 2)` (Not Null). Default: `0.00`.
  - `target_date`: `DATE` (Not Null). Targeted completion date.
  - `status`: `VARCHAR(50)` (Not Null). Default: `'active'`.
  - `created_at`: `TIMESTAMP WITH TIME ZONE` (Not Null). Default: `CURRENT_TIMESTAMP`.
  - `updated_at`: `TIMESTAMP WITH TIME ZONE` (Not Null). Default: `CURRENT_TIMESTAMP`.
* **Constraints:**
  - `PK_goals`: Primary key on `goal_id`.
  - `FK_goals_users`: Foreign key `user_id` referencing `users.id` with `ON DELETE CASCADE`.
  - `CK_goals_target_positive`: Check constraint `target_amount > 0`.
  - `CK_goals_saved_nonnegative`: Check constraint `saved_amount >= 0`.
  - `CK_goals_status`: Check constraint `status IN ('active', 'completed', 'failed')`.
* **Relationships:**
  - Belongs to a user (`N:1`).

---

### 2.5 Recommendations (`recommendations`)
* **Purpose:** Stores personalized, AI-calculated recommendations for optimizing spending habits.
* **Fields:**
  - `recommendation_id`: `UUID` (Primary Key).
  - `user_id`: `UUID` (Not Null, Foreign Key).
  - `recommendation_type`: `VARCHAR(100)` (Not Null). Category being addressed (e.g. Subscriptions).
  - `severity`: `VARCHAR(20)` (Not Null). Severity level of the issue.
  - `possible_savings`: `NUMERIC(12, 2)` (Not Null). Potential monthly savings.
  - `confidence`: `DOUBLE PRECISION` (Not Null). Model confidence.
  - `recommendation`: `TEXT` (Not Null). Actionable recommendation text.
  - `reason`: `TEXT` (Not Null). Detailed logical reasoning.
  - `status`: `VARCHAR(50)` (Not Null). Default: `'active'`.
  - `created_at`: `TIMESTAMP WITH TIME ZONE` (Not Null). Default: `CURRENT_TIMESTAMP`.
  - `updated_at`: `TIMESTAMP WITH TIME ZONE` (Not Null). Default: `CURRENT_TIMESTAMP`.
* **Constraints:**
  - `PK_recommendations`: Primary key on `recommendation_id`.
  - `FK_recommendations_users`: Foreign key `user_id` referencing `users.id` with `ON DELETE CASCADE`.
  - `CK_rec_severity`: Check constraint `severity IN ('Low', 'Medium', 'High')`.
  - `CK_rec_confidence`: Check constraint `confidence >= 0.0 AND confidence <= 1.0`.
  - `CK_rec_status`: Check constraint `status IN ('active', 'accepted', 'dismissed', 'applied')`.
* **Relationships:**
  - Belongs to a user (`N:1`).

---

### 2.6 Alerts (`alerts`)
* **Purpose:** Financial system notifications (e.g. budget exceed warnings, goal milestones reached).
* **Fields:**
  - `alert_id`: `UUID` (Primary Key).
  - `user_id`: `UUID` (Not Null, Foreign Key).
  - `type`: `VARCHAR(50)` (Not Null). Notification type.
  - `title`: `VARCHAR(255)` (Not Null). Short summary.
  - `message`: `TEXT` (Not Null). Alert body text.
  - `is_read`: `BOOLEAN` (Not Null). Default: `FALSE`.
  - `created_at`: `TIMESTAMP WITH TIME ZONE` (Not Null). Default: `CURRENT_TIMESTAMP`.
  - `updated_at`: `TIMESTAMP WITH TIME ZONE` (Not Null). Default: `CURRENT_TIMESTAMP`.
* **Constraints:**
  - `PK_alerts`: Primary key on `alert_id`.
  - `FK_alerts_users`: Foreign key `user_id` referencing `users.id` with `ON DELETE CASCADE`.
* **Relationships:**
  - Belongs to a user (`N:1`).

---

### 2.7 Personality Profiles (`personality_profiles`)
* **Purpose:** Stores the calculated financial personality DNA profile of the user.
* **Fields:**
  - `profile_id`: `UUID` (Primary Key).
  - `user_id`: `UUID` (Not Null, Foreign Key).
  - `personality_type`: `VARCHAR(100)` (Not Null). Archetype category.
  - `description`: `TEXT` (Not Null). Detailed description of the user's financial personality.
  - `traits`: `JSONB` (Not Null). Document schema storing strengths and weaknesses:
    `{"strengths": ["...", "..."], "weaknesses": ["...", "..."]}`
  - `investment_style`: `TEXT` (Not Null). Suggested investment profile description.
  - `compatibility_tips`: `TEXT` (Nullable). Behavioral tips.
  - `assessed_at`: `TIMESTAMP WITH TIME ZONE` (Not Null). Default: `CURRENT_TIMESTAMP`.
  - `created_at`: `TIMESTAMP WITH TIME ZONE` (Not Null). Default: `CURRENT_TIMESTAMP`.
  - `updated_at`: `TIMESTAMP WITH TIME ZONE` (Not Null). Default: `CURRENT_TIMESTAMP`.
* **Constraints:**
  - `PK_personality_profiles`: Primary key on `profile_id`.
  - `FK_personality_profiles_users`: Foreign key `user_id` referencing `users.id` with `ON DELETE CASCADE`.
  - `UQ_personality_profiles_user`: Unique constraint on `user_id` to enforce a 1:1 user-to-profile mapping.
* **Relationships:**
  - Belongs to a user (`1:1`).

---

### 2.8 Stress Scores (`stress_scores`)
* **Purpose:** Tracks historical financial stress assessments calculated over time.
* **Fields:**
  - `assessment_id`: `UUID` (Primary Key).
  - `user_id`: `UUID` (Not Null, Foreign Key).
  - `stress_score`: `DOUBLE PRECISION` (Not Null). Stress score index (0-100).
  - `stress_category`: `VARCHAR(50)` (Not Null). Stress classification tier.
  - `factors`: `JSONB` (Not Null). Underlying metric variables (debt ratios, savings rate index, volatility).
  - `action_steps`: `JSONB` (Not Null). List of personalized mitigation steps (`["Step 1", "Step 2"]`).
  - `assessed_at`: `TIMESTAMP WITH TIME ZONE` (Not Null). Default: `CURRENT_TIMESTAMP`.
  - `created_at`: `TIMESTAMP WITH TIME ZONE` (Not Null). Default: `CURRENT_TIMESTAMP`.
  - `updated_at`: `TIMESTAMP WITH TIME ZONE` (Not Null). Default: `CURRENT_TIMESTAMP`.
* **Constraints:**
  - `PK_stress_scores`: Primary key on `assessment_id`.
  - `FK_stress_scores_users`: Foreign key `user_id` referencing `users.id` with `ON DELETE CASCADE`.
  - `CK_stress_range`: Check constraint `stress_score >= 0.0 AND stress_score <= 100.0`.
  - `CK_stress_category`: Check constraint `stress_category IN ('Low', 'Moderate', 'High', 'Severe')`.
* **Relationships:**
  - Belongs to a user (`N:1`).

---

### 2.9 Chat History (`chat_history`)
* **Purpose:** Persists historical chat logs with the AI assistants.
* **Fields:**
  - `message_id`: `UUID` (Primary Key).
  - `user_id`: `UUID` (Not Null, Foreign Key).
  - `session_id`: `VARCHAR(100)` (Not Null). Groups conversational messages within a session.
  - `assistant_type`: `VARCHAR(50)` (Not Null). Identifies the assistant type (`'general'` or `'investment'`).
  - `sender`: `VARCHAR(20)` (Not Null). The sender of the message.
  - `message`: `TEXT` (Not Null). Message body.
  - `metadata`: `JSONB` (Nullable). Audit trail context flags (e.g. topic tags, context injection states).
  - `created_at`: `TIMESTAMP WITH TIME ZONE` (Not Null). Default: `CURRENT_TIMESTAMP`.
* **Constraints:**
  - `PK_chat_history`: Primary key on `message_id`.
  - `FK_chat_history_users`: Foreign key `user_id` referencing `users.id` with `ON DELETE CASCADE`.
  - `CK_chat_sender`: Check constraint `sender IN ('user', 'assistant')`.
  - `CK_chat_assistant_type`: Check constraint `assistant_type IN ('general', 'investment')`.
* **Relationships:**
  - Belongs to a user (`N:1`).

---

## 3. Keys and Constraints

* **Primary Keys:** Every table uses a globally unique `UUIDv4` identifier generated at insertion (`gen_random_uuid()`). This prevents ID predictability and facilitates offline generation.
* **Foreign Keys:** References are enforced with relational integrity. In most scenarios, user-dependent child tables implement `ON DELETE CASCADE`. This ensures GDPR/privacy compliance (deleting a user account cleans up all associated records in child tables).
* **Unique Constraints:** Enforced on `users(email)`, `budgets(user_id, category)`, and `personality_profiles(user_id)`.

---

## 4. Indexing Strategy

To speed up query execution and maintain quick response times, we implement the following indexes:

### 4.1 Foreign Key Indexes
PostgreSQL does not index foreign keys by default. We explicitly define index structures on all foreign keys to speed up join operations:
```sql
CREATE INDEX idx_expenses_user_id ON expenses(user_id);
CREATE INDEX idx_budgets_user_id ON budgets(user_id);
CREATE INDEX idx_goals_user_id ON goals(user_id);
CREATE INDEX idx_recommendations_user_id ON recommendations(user_id);
CREATE INDEX idx_alerts_user_id ON alerts(user_id);
CREATE INDEX idx_stress_scores_user_id ON stress_scores(user_id);
CREATE INDEX idx_chat_history_user_id ON chat_history(user_id);
```

### 4.2 Composite Indexes
Designed to optimize multi-column filter criteria:
```sql
-- Speed up expense listing filters by user, date ranges, and categories
CREATE INDEX idx_expenses_user_date_cat ON expenses(user_id, transaction_date DESC, category);

-- Speed up search on user active recommendations
CREATE INDEX idx_recommendations_user_status ON recommendations(user_id, status) WHERE status = 'active';

-- Speed up unread alert fetches
CREATE INDEX idx_alerts_user_unread ON alerts(user_id) WHERE is_read = FALSE;
```

### 4.3 JSONB Indexing (GIN)
Allows deep indexing of unstructured properties stored within `JSONB` fields:
```sql
-- Speed up search queries in chat histories
CREATE INDEX idx_chat_history_metadata_gin ON chat_history USING gin (metadata);
```

---

## 5. Normalization

* **First Normal Form (1NF):** Achieved. Every cell contains atomic values. All table layouts represent relations with fixed attributes.
* **Second Normal Form (2NF):** Achieved. There are no partial dependencies; all non-key columns depend entirely on their primary keys.
* **Third Normal Form (3NF):** Achieved. There are no transitive dependencies; every non-prime attribute depends only on the primary key.
* **Denormalization Trade-offs:**
  - Budgets do not store cached metrics (like current spending or remaining balances) in their schemas. Instead, these are aggregated dynamically in memory or SQL queries using joins with `expenses`. This prevents data anomalies.

---

## 6. Query Optimization Recommendations

* **Cursor-Based Pagination:** Instead of using slow `OFFSET` clauses for pagination (which gets slower as offset size increases), use cursor-based pagination filtering on dates or IDs (e.g. `WHERE transaction_date < :last_date`).
* **Aggregate Functions with Window Rules:** When calculating cumulative monthly totals, use window functions:
  ```sql
  SELECT amount, transaction_date,
         SUM(amount) OVER (PARTITION BY category ORDER BY transaction_date) as running_total
  FROM expenses
  WHERE user_id = :user_id;
  ```
* **Partitioning:** For large databases, partition the `expenses` table by year-month ranges. This keeps indexes small and speeds up scans by querying only the relevant partitions:
  ```sql
  CREATE TABLE expenses (
      expense_id UUID NOT NULL,
      user_id UUID NOT NULL,
      amount NUMERIC(12, 2) NOT NULL,
      transaction_date DATE NOT NULL,
      ...
  ) PARTITION BY RANGE (transaction_date);
  ```
* **Vacuuming Policies:** Schedule regular `VACUUM ANALYZE` operations on highly updated tables (`expenses`, `chat_history`) to clean up dead rows and update query statistics.
