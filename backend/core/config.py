from pydantic_settings import BaseSettings
from pydantic import field_validator

class Settings(BaseSettings):
    API_PREFIX: str = "/api"

    DEBUG: bool = False

    DATABASE_URL: str

    ALLOWED_ORIGINS: str = ""
    ALLOWED_ORIGINS_DEV: str = ""

    USER_AGENT: str = ""
    LANGCHAIN_TRACING_V2: str = "true"
    LANGCHAIN_ENDPOINT: str
    LANGCHAIN_API_KEY: str
    TAVILY_API_KEY: str
    OPENAI_API_KEY: str
    BRAINTRUST_API_KEY: str

    @field_validator("ALLOWED_ORIGINS")
    def parse_allowed_origins(cls, v: str) -> list[str]:
        return v.split(",") if v else []
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_senstive = True

settings = Settings()


