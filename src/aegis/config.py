import os
from functools import lru_cache
from pathlib import Path
from typing import Any, Literal

from pydantic import DirectoryPath, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict

from aegis.domain.base import SCHEMA_VERSION


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="AEGIS_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="forbid",
        frozen=True,
    )

    environment: Literal["local", "demo"] = "local"
    app_version: str = "0.1.0"
    schema_version: str = SCHEMA_VERSION
    synthetic_data_dir: DirectoryPath = Path("data/synthetic")

    def __init__(self, **values: Any) -> None:
        known_env_vars = {f"AEGIS_{field_name.upper()}" for field_name in type(self).model_fields}
        unexpected_env_vars = {
            name for name in os.environ if name.startswith("AEGIS_") and name not in known_env_vars
        }
        if unexpected_env_vars:
            raise ValidationError.from_exception_data(
                type(self).__name__,
                [
                    {
                        "type": "extra_forbidden",
                        "loc": (name,),
                        "input": "<redacted>",
                    }
                    for name in sorted(unexpected_env_vars)
                ],
            )
        super().__init__(**values)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
