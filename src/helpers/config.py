from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name:str
    app_version:str
    FILE_ALLOWED_TYPES:list
    FILE_SIZE_MAX:int
    FILE_DEFAULT_CHUNK_SIZE:int


    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT:int
    POSTGRES_MAIN_DATABASE: str

    class Config:
        env_file = ".env"




def get_settings():
    return Settings()