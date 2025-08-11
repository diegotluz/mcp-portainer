from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    portainer_url: str
    portainer_api_key: str

    class Config:
        env_file = ".env"

settings = Settings()  # Make sure .env file exists and contains PORTAINER_URL and PORTAINER_API_KEY