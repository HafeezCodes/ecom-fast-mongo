from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # MongoDB Local
    # MONGODB_HOST: str
    # MONGODB_PORT: int
    # MONGODB_USERNAME: str
    # MONGODB_PASSWORD: str
    # MONGODB_DB: str
    
    # MongoDB online
    MONGODB_URI: str

    # JWT
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    
    class Config:
        env_file = ".env"

settings = Settings()
