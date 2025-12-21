from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # Application settings
    app_env: str = "development"
    port: int = 8000
    
    # Database settings
    mongodb_uri: str
    
    # JWT settings
    jwt_secret: str
    jwt_expires_in: int = 86400  # 24 hours in seconds
    
    # CORS settings
    cors_origins: str = "http://localhost:3000"
    
    # SendGrid settings
    sendgrid_api_key: str = ""
    sendgrid_from_email: str = ""
    
    @property
    def cors_origins_list(self) -> list[str]:
        """Convert comma-separated CORS origins to list."""
        return [origin.strip() for origin in self.cors_origins.split(",")]


# Global settings instance
settings = Settings()