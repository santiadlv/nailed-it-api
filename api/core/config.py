from pydantic import BaseSettings
from secrets import token_urlsafe

class Settings(BaseSettings):
    SECRET_KEY: str = token_urlsafe(32)
    PROJECT_NAME: str
    ADMIN_EMAIL: str
    MONGODB_URL: str
    MONGODB_NAME: str
    MONGODB_COLLECTION: str
    MONGODB_COLLECTION_SALONS: str
    MONGODB_COLLECTION_SERVICES: str
    MONGODB_COLLECTION_RESERVATIONS: str

    MONGODB_COLLECTION_HOURS: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

settings = Settings()