from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name:str
    app_version:str
    FILE_ALLOWED_TYPES:str
    FILE_SIZE_MAX:int


    class config:
        env_file = ".env"




def get_settings():
    return Settings()