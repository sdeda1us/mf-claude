from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "sqlite:///./megafantasy.db"
    jwt_secret: str = "dev-secret-change-me"
    jwt_algorithm: str = "HS256"
    magic_link_ttl_minutes: int = 15
    session_ttl_days: int = 30

    resend_api_key: str | None = None
    email_from: str = "Megafantasy <onboarding@resend.dev>"

    # Public base URL used to build magic-link URLs sent in email
    app_base_url: str = "http://localhost:5173"
    # Where the API is served from (used by the /auth/verify redirect target)
    api_base_url: str = "http://localhost:8000"

    # Comma-separated allow-list of the 6 league members, e.g. "a@x.com,b@x.com"
    allowed_emails: str = ""

    cookie_secure: bool = False

    @property
    def allowed_email_list(self) -> list[str]:
        return [e.strip().lower() for e in self.allowed_emails.split(",") if e.strip()]


settings = Settings()
