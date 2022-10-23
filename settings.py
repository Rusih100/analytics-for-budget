from pydantic import BaseSettings, SecretStr


class Settings(BaseSettings):
    TELEGRAM_TOKEN: SecretStr
    SPREADHEET_ID: SecretStr

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
