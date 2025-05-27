import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    MONGO_URI: str = os.getenv("MONGO_URI")
    DATABASE_NAME: str = os.getenv("DB_NAME")
    HF_API_KEY: str = os.getenv("HF_API_KEY")

settings = Settings()