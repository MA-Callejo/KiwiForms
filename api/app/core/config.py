from pathlib import Path
from typing import Any, Dict, List, Optional, Union
import os
from pydantic import AnyHttpUrl, EmailStr, HttpUrl, PostgresDsn, validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()
# Ruta absoluta al .env en la raíz del proyecto (config.py -> core -> app -> raíz)
ENV_FILE = Path(__file__).resolve().parents[2] / ".env"


class Settings(BaseSettings):
    DATABASEUSER: str = os.getenv("DATABASEUSER")
    DATABASE: str = os.getenv("DATABASE")
    DATABASEHOST: str = os.getenv("DATABASEHOST")
    DATABASEPASS: str = os.getenv("DATABASEPASS")
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "f8561f0b77d313034f2ab5f9ba265b276cc4b43081c131134ef7c2661c55526b"
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    PROJECT_NAME: str = "KiwiForms - API"

    IMAGENES_DIR: str = "/var/www/wellit/imagenes"
    IMAGENES_BASE_URL: str = "https://gestionenmoviment.es/wellit/imagenes"

    # SQLALCHEMY_DATABASE_URI: Optional[str] = 'mariadb+mariadbconnector://remoto:Desa2012@121.227.104.63:3306/forms'
    SQLALCHEMY_DATABASE_URI: Optional[str] = 'mariadb+mariadbconnector://'+DATABASEUSER+':'+DATABASEPASS+'@'+DATABASEHOST+':3306/'+DATABASE
    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE),
        env_file_encoding="utf-8",
        extra="ignore",  # ignora otras variables del .env que no declares aquí
    )


settings = Settings()
