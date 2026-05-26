from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.core.config import settings
from app.core.limiter import limiter
from app.api.v1.auth import router as auth_router
from app.api.v1.expenses import router as expenses_router
from app.api.v1.budgets import router as budgets_router
from app.api.v1.goals import router as goals_router

app = FastAPI(
    title="MoneyMind X API",
    description="Core backend for MoneyMind X personal finance API",
    version="1.0.0"
)

# Wire up the rate limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS configuration
origins = settings.ALLOWED_ORIGINS
if isinstance(origins, str):
    origins = [origins]

# Ensure "*" is not allowed in production if needed, but here we strictly use the configured list.
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix="/api/v1")
app.include_router(expenses_router, prefix="/api/v1")
app.include_router(budgets_router, prefix="/api/v1")
app.include_router(goals_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Welcome to MoneyMind X API"}
