# MoneyMind X - 4-Week Sprint Planning

This document details the 4-week sprint delivery plan for **MoneyMind X**. The plan is structured around a team of four specialized developers, executing weekly milestones from initial setup to deployment.

---

## Team Roles & Allocations

* **Dev A (Lead Backend Engineer):** Handles database schemas, FastAPI API routes, JWT security, and repo access layers.
* **Dev B (Lead Frontend Engineer):** Handles Next.js application routes, Zustand state logic, form validation, and Tailwind CSS.
* **Dev C (AI & ML Specialist):** Handles Gemini integration, Python analytics models (stress indices, personality types, compounding simulations).
* **Dev D (DevOps & QA Engineer):** Handles CI/CD pipelines, unit testing suites, Docker configuration, load testing, and cloud infrastructure setup.

---

## Week 1: Planning & Setup

### Week 1 Sprint Goals
Establish the backend service skeletons, deploy initial database migrations, design the Next.js visual layouts, and verify API connection paths.

### Week 1 Tasks & Assignments
| Task ID | Task Name | Description | Assignee | Dependencies |
|---|---|---|---|---|
| **TSK-101** | Database Schema Creation | Apply PostgreSQL database schemas (Users, Expenses, Budgets, Goals). | Dev A | None |
| **TSK-102** | JWT Auth Implementation | Code `/auth/register` and `/auth/login` endpoints on the FastAPI backend. | Dev A | TSK-101 |
| **TSK-103** | Next.js Base Setup | Initialize the Next.js framework, configure Tailwind CSS, and set up the App Router. | Dev B | None |
| **TSK-104** | API Fetch Client | Code the frontend fetch API wrapper with automatic bearer token inject interceptors. | Dev B | TSK-102 |
| **TSK-105** | Gemini & ML Setup | Set up local credentials for the Gemini API and write service wrappers. | Dev C | None |
| **TSK-106** | CI/CD & Docker Setup | Configure local Docker containers and verify Github Actions workflow paths. | Dev D | None |

### Week 1 Deliverables
* Integrated local development environment (Docker Compose running PostgreSQL, FastAPI, Next.js).
* Successful JWT registration and login pipelines verified with unit tests.
* Responsive Tailwind client layout shell with state routing.

### Week 1 Risks & Mitigation
* **Risk:** Delayed Gemini API key access.
* **Mitigation:** Dev C will write mock interface stubs return predefined JSON payloads to keep development moving.

---

## Week 2: Core Development

### Week 2 Sprint Goals
Complete the core CRUD operations for Expenses, Budgets, and Goals on both frontend and backend, ensuring database constraints match client forms.

### Week 2 Tasks & Assignments
| Task ID | Task Name | Description | Assignee | Dependencies |
|---|---|---|---|---|
| **TSK-201** | Expenses API | Create core `/expenses` CRUD endpoints on the backend. | Dev A | TSK-102 |
| **TSK-202** | Budgets & Goals API | Create `/budgets` and `/goals` CRUD endpoints on the backend. | Dev A | TSK-201 |
| **TSK-203** | Expense Dashboard | Build frontend pages for logging and filtering expenses. | Dev B | TSK-103 |
| **TSK-204** | Budgets & Goals UI | Build frontend interfaces to track budgets and savings goals. | Dev B | TSK-203 |
| **TSK-205** | Budget Exceed Alerts | Code backend check rules to trigger alert logs when expense limits are exceeded. | Dev C | TSK-202 |
| **TSK-206** | Database Index Optimization | Review Postgres metrics and add foreign key/composite indexes on `expenses` and `budgets`. | Dev D | TSK-201 |

### Week 2 Deliverables
* Functional Expenses, Budgets, and Goals management dashboards connected to database tables.
* Working alerts engine that registers notifications in the database when categories exceed monthly limits.

### Week 2 Risks & Mitigation
* **Risk:** Performance bottlenecks on backend queries due to large expense counts.
* **Mitigation:** Dev D will implement B-Tree index arrays on `(user_id, transaction_date DESC, category)` to speed up filter queries.

---

## Week 3: AI Development

### Week 3 Sprint Goals
Incorporate the Gemini AI Chat Assistant, calculate stress metrics, run personality profile assessments, and deploy compound growth projections in the wealth simulator.

### Week 3 Tasks & Assignments
| Task ID | Task Name | Description | Assignee | Dependencies |
|---|---|---|---|---|
| **TSK-301** | Recommendations Engine | Code rules to evaluate spending metrics and return saving recommendations. | Dev C | TSK-202 |
| **TSK-302** | Stress Score Assessment | Build calculations to score financial stress based on saving rates, debts, and stability factors. | Dev C | TSK-301 |
| **TSK-303** | Personality DNA Quiz | Build the 10-question questionnaire backend engine and UI client layouts. | Dev C, Dev B | TSK-104 |
| **TSK-304** | Wealth Simulator API | Build compound growth simulations based on custom deposits, inflation, and rate targets. | Dev A, Dev C | TSK-202 |
| **TSK-305** | AI Chat Assistants | Integrate Gemini educational assistant chat interfaces. | Dev C, Dev B | TSK-105 |
| **TSK-306** | Mock-up Testing Arrays | Set up stress testing scripts for simultaneous requests to the Gemini API routes. | Dev D | TSK-305 |

### Week 3 Deliverables
* Functioning AI assistants with system prompts configured to prevent financial advice liability.
* Interactive Wealth Simulator and Personality DNA quiz modules.
* Stress scoring engine calculations delivering categorized mitigation steps.

### Week 3 Risks & Mitigation
* **Risk:** High latency from Gemini API requests slows down chat response times.
* **Mitigation:** Implement streaming responses or run long-running analytics (like recommendations) as async tasks.

---

## Week 4: Testing & Deployment

### Week 4 Sprint Goals
Conduct extensive integration testing, achieve >80% test coverage, set up rate limits, build production containers, and deploy to staging and production cloud infrastructure.

### Week 4 Tasks & Assignments
| Task ID | Task Name | Description | Assignee | Dependencies |
|---|---|---|---|---|
| **TSK-401** | End-to-End Integration | Validate all data flows (Frontend -> Backend -> DB / AI) across target user flows. | Dev B, Dev D | All Week 3 Tasks |
| **TSK-402** | Rate Limiting Enforcement | Set up SlowAPI rules (10/min for auth, 60/min for chat, 100/min standard). | Dev A | TSK-102 |
| **TSK-403** | Vulnerability Scan | Conduct OWASP testing to verify JWT signatures and prevent SQL injection. | Dev D | TSK-401 |
| **TSK-404** | Next.js Production Build | Build and optimize the Next.js client bundle. | Dev B | TSK-401 |
| **TSK-405** | Production Deploy | Deploy application containers to AWS ECS behind an Application Load Balancer. | Dev D | TSK-404 |
| **TSK-406** | Monitoring Alerts | Set up monitoring (CloudWatch/Datadog) to alert on HTTP 500 status codes. | Dev D | TSK-405 |

### Week 4 Deliverables
* Deployed production environments (Frontend on Vercel/AWS CloudFront, backend containers on ECS, database on RDS).
* Uptime monitoring alerts configured.
* Security audit sign-off showing zero high-severity vulnerabilities.

### Week 4 Risks & Mitigation
* **Risk:** Next.js build errors during production build optimization.
* **Mitigation:** Run daily checks in CI/CD pipelines starting in Week 2 to catch build errors early.

---

## Cross-Week Dependencies

```
+--------------------+        +--------------------+        +--------------------+
|  W1: Setup         |        |  W2: Core          |        |  W3: AI & Analytics|
|  - TS Base Schema  |=======>|  - CRUD APIs       |=======>|  - Recommend Engine|
|  - App Interceptor |        |  - Dashboard UI    |        |  - Stress Scores   |
+--------------------+        +--------------------+        +--------------------+
                                                                      ||
                                                                      ||
                                                                      v
                                                            +--------------------+
                                                            |  W4: Testing & Dep |
                                                            |  - E2E Validation  |
                                                            |  - Cloud Deployment|
                                                            +--------------------+
```

---

## Definition of Done (DoD)

A user story or task is marked as **Done** only when it meets the following criteria:
1. **Code Quality:** Code compiles successfully and passes static analysis checks (e.g. Flake8, Ruff for backend; ESLint, Prettier for frontend).
2. **Review:** Code is reviewed and approved by at least one other developer.
3. **Test Coverage:** Automated unit test coverage is above 80%.
4. **Integration:** Code is merged into the main development branch and verified in a staging environment.
5. **Security:** No critical or high-severity vulnerabilities are flagged by dependency scanners.
6. **Documentation:** API specifications, database design documents, and setup guides are updated.
7. **Accessibility:** Frontend interfaces pass basic accessibility checks (e.g., WCAG 2.1 AA compatibility).
