import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Smart Recruiter API"
    # PostgreSQL connection settings
    database_url: str = (
        "postgresql+psycopg://smartrecruiter:smartrecruiter@localhost:5433/smartrecruiter"
    )
    # Override via DATABASE_URL env var or backend/.env
    database_url_env: str = "DATABASE_URL"

    jwt_secret: str = "dev-secret-change-me"
    codewars_base_url: str = "https://www.codewars.com/api/v1"

    # Email / SMTP settings for invitation emails.
    smtp_host: str = "localhost"
    smtp_port: int = 587
    smtp_username: str | None = None
    smtp_password: str | None = None
    smtp_use_tls: bool = True
    sender_email: str = "noreply@smartrecruiter.com"
    sender_name: str = "Smart Recruiter"
    frontend_base_url: str = "http://localhost:5173"
    # API base URL for the frontend (used by the frontend to connect to backend)
    api_base_url: str = "http://localhost:5000/api"

    class Config:
        env_file = ".env"


if settings.jwt_secret == "dev-secret-change-me" and os.getenv("ENVIRONMENT") == "production":
    raise RuntimeError(
        "JWT_SECRET must be set to a secure value in production. "
        "Set the JWT_SECRET env var to a strong random string."
    )


# Production-specific settings
PRODUCTION = os.getenv("ENVIRONMENT", "development") == "production"
if PRODUCTION:
    # Disable debug mode in production
    settings.debug = False
    # Enable detailed logging
    settings.log_level = "INFO"
    # Increase connection pool size for production
    settings.db_pool_size = 20
    # Enable PostgreSQL SSL
    settings.database_url += "?sslmode=require"
