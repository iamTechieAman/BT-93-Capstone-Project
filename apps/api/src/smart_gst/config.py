"""
Unified Pydantic Settings Configuration for Smart GST API.
All environment reads MUST occur in this file only.
"""

from typing import Any, Optional, Union

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Application
    APP_NAME: str = "Smart GST API"
    APP_VERSION: str = "0.1.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = False

    # Database & Storage
    DATABASE_URL: str = Field(
        default="sqlite:///./smart_gst.db",
        description="PostgreSQL / SQLite database connection URL",
    )

    # Authentication & JWT
    JWT_SECRET_KEY: str = Field(
        default="smart_gst_secure_secret_key_change_in_production_32bytes",
        description="HMAC-SHA256 signature key for JWT tokens",
    )
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # CORS
    CORS_ORIGINS: Union[list[str], str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
    ]

    @field_validator("CORS_ORIGINS", mode="after")
    @classmethod
    def assemble_cors_origins(cls, v: Any) -> list[str]:
        if isinstance(v, str):
            if v.startswith("["):
                import json

                return json.loads(v)
            return [i.strip() for i in v.split(",") if i.strip()]
        return v

    # AI & Explainability
    GEMINI_API_KEY: Optional[str] = None
    CONFIDENCE_THRESHOLD: float = 80.0

    # GSTIN Verification Providers
    GST_PROVIDER_API_KEY: Optional[str] = None
    GST_PROVIDER_URL: str = "https://api.gst.gov.in/taxpayer"
    GST_PROVIDER_NAME: str = "Licensed GSP Service"
    GST_PROVIDER_TIMEOUT_SEC: int = 5
    GST_CACHE_TTL_HOURS: int = 24

    # Feature Flags
    ENABLE_NEO4J: bool = False
    NEO4J_URI: str = "bolt://localhost:7687"
    NEO4J_USER: str = "neo4j"
    NEO4J_PASSWORD: str = "password123"


settings = Settings()
