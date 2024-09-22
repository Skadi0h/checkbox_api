import enum

from pydantic import PostgresDsn, Field
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class RunModes(enum.StrEnum):
    DEVELOPMENT = enum.auto()
    PRODUCTION = enum.auto()


class PostgreSQLConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='PG_')

    db_user_name: str = Field(
        default='user_name'
    )
    db_user_password: str = Field(
        default='user_password'
    )
    db_host: str = Field(
        default='postgres'
    )
    db_port: int = Field(
        default=5432
    )
    db_name: str = Field(
        default='db'
    )

    @property
    def db_uri(self) -> PostgresDsn:
        return MultiHostUrl.build(
            scheme='postgresql+asyncpg',
            username=self.db_user_name,
            password=self.db_user_password,
            host=self.db_host,
            port=self.db_port,
            
        )


class ApplicationConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='APP_')
    run_mode: RunModes = Field(default=RunModes.DEVELOPMENT)
    allowed_hosts: list[str] = Field(
        default=['localhost']
    )


POSTGRES_CONFIG = PostgreSQLConfig()
APP_CONFIG = ApplicationConfig()
