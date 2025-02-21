from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    OPENAI_API_KEY: str
    MINIO_HOST: str
    MINIO_CUSTOM_PORT: int
    MINIO_ROOT_USER: str
    MINIO_ROOT_PASSWORD: str
    MINIO_PUBLIC_BUCKET_WHITELIST: list[str] = ["fastapi-minio"]

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
