from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name:str
    app_version:str

    POSTING_ALLOWED_TYPES:list
    POSTING_SIZE_MAX:int
    POSTING_DEFAULT_CHUNK_SIZE:int

    EXPERIENCE_ALLOWED_TYPES: list
    EXPERIENCE_SIZE_MAX:int
    EXPERIENCE_DEFAULT_CHUNK_SIZE:int


    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT:int
    POSTGRES_MAIN_DATABASE: str
    
    GENERATION_PROVIDER:str
    EMBEDDING_PROVIDER:str
    GENERATION_MODEL :str
    EMBEDDING_MODEL :str
    
    OPENAI_API_KEY:str
    OPENAI_API_URL:str
    GEMINI_API_KEY:str

    INPUT_DEFAULT_MAX_CHARACTERS:int
    GENERATION_DEFAULT_MAX_TOKENS:int
    GENERATION_DEFAULT_TEMPERATURE:float

    VECTOR_DB_BACKEND_LITERAL :list
    VECTOR_DB_BACKEND : str 
    VECTOR_DB_PATH: str
    VECTOR_DB_DISTANCE_METHOD: str
    VECTOR_DB_PGVEC_INDEX_THRESHOLD : int

    PRIMARY_LANG: str
    DEFAULT_LANG: str
    class Config:
        env_file = ".env"




def get_settings():
    return Settings()