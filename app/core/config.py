from pydantic import BaseSettings
from typing import Optional


MAX_SYM_NAME = 100
MAX_NAME_IN_REPR = 6


class Settings(BaseSettings):
    app_title: str = 'QRKot'
    app_description: str = 'Сервис пожертвований для кошек'
    database_url: str = 'sqlite+aiosqlite:///./qrcat.db'
    secret: str = 'SECRET'

    """Данные для GoogleAPI"""
    email: Optional[str] = None
    type: Optional[str] = None
    project_id: Optional[str] = None
    private_key_id: Optional[str] = None
    private_key: Optional[str] = None
    client_email: Optional[str] = None
    client_id: Optional[str] = None
    auth_uri: Optional[str] = None
    token_uri: Optional[str] = None
    auth_provider_x509_cert_url: Optional[str] = None
    client_x509_cert_url: Optional[str] = None

    class Config:
        env_file = '.env'


settings = Settings()
