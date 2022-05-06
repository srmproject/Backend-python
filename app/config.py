from typing import Optional
from pydantic import BaseSettings, Field


class GlobalConfig(BaseSettings):
    """공통 설정"""
    ENV_STATE: str = Field("dev", env="MODE")

    POSTGRESQL_HOST: Optional[str] = None
    POSTGRESQL_USER: Optional[str] = None
    POSTGRESQL_PASSWORD: Optional[str] = None

    class Config:
        """BaseSettings 설정"""
        env_file: str = ".env"

class DevConfig(GlobalConfig):
    """개발 설정"""
    class Config:
        """BaseSettings 설정"""
        env_prefix: str = "DEV_"

class ProdConfig(GlobalConfig):
    """운영 설정"""
    class Config:
        """BaseSettings 설정"""
        env_prefix: str = "PROD_"

class FactoryConfig:
    """설정 로드"""
    def __init__(self, env_state: Optional[str]):
        self.env_state = env_state

    def __call__(self):
        if self.env_state == "dev":
            return DevConfig()

        elif self.env_state == "prod":
            return ProdConfig()


cnf = FactoryConfig(GlobalConfig().ENV_STATE)()