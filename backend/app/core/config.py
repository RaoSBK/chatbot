from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://moneymindx:password123@localhost/moneymindx"
    JWT_SECRET: str = "supersecretjwttokenkey123!"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    GEMINI_API_KEY: str = "api_key_placeholder"

    class Config:
        env_file = ".env"

settings = Settings()
