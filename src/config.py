from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

BASE_DIR = Path(__file__).parent.parent
env_file = BASE_DIR / ".env"

load_dotenv(env_file)

class EnvSettings(BaseSettings):
    BOT_TOKEN: str
    DB_NAME: str
    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: str

    @property
    def DATABASE_DSN(self) -> str:
        return f"postgresql://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    model_config = SettingsConfigDict(
        env_file='.env',  # Файл з змінними середовища
    )

class Settings(BaseSettings):
    env: EnvSettings = EnvSettings()

settings = Settings()
