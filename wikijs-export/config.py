from pathlib import Path

from pydantic import BaseSettings

env_location = Path(".env").resolve()
BASE_DIR = Path(".")

class Settings(BaseSettings):
   db_host: str
   db_user: str
   db_password: str
   db_database: str
   db_port: str

   class Config:
      env_file = env_location
      env_file_encoding = 'utf-8'