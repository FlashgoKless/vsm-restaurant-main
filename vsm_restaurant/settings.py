from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    db_url: str = "postgresql+psycopg://postgres:5FCCBA11-B16E-4C47-BFDF-06051C17226D@127.0.0.1:5432/vsm_restaurant"
    # Static token for admin endpoints (Authorization: Bearer <token>)
    admin_token: str = "changeme"

    model_config = SettingsConfigDict(env_file="config.env")
