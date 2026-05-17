from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    anthropic_api_key: str
    openai_api_key: str = ""
    database_url: str = "sqlite+aiosqlite:///./patternai.db"
    upload_dir: Path = Path("./uploads")
    export_dir: Path = Path("./exports")

    model_config = {"env_file": ".env"}


settings = Settings()

settings.upload_dir.mkdir(exist_ok=True)
settings.export_dir.mkdir(exist_ok=True)
