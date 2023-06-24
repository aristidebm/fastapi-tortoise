import os
import re
import zoneinfo
from logging.config import dictConfigClass
from pathlib import Path, PosixPath

import yaml
from pydantic import (
    BaseSettings,
    FilePath,
    HttpUrl,
    PostgresDsn,
    fields,
    root_validator,
    validator,
)
from src.constants import Environment, SQLiteDsn

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    ENVIRONMENT: Environment = fields.Field(Environment.DEV)
    DSN: PostgresDsn | SQLiteDsn = "sqlite:///:memory:"
    USE_TZ: bool = True
    TIMEZONE: str | None = None
    TORTOISE_ORM: dict | FilePath = BASE_DIR / "tortoise.yml"
    LOGGERS: dict | dictConfigClass | FilePath = BASE_DIR / "loggers.yml"
    CORS_ALLOW_ORIGINS: list[HttpUrl] = [
        "http://127.0.0.1",
    ]
    CORS_ALLOW_HEADERS: list = []
    CORS_ALLOW_METHODS: list = []

    class Config:
        case_sensitive = True
        env_file = ".env"
        fields = {"DSN": {"env": "DATABASE_URL"}}

    @validator("TIMEZONE")
    def validate_timezone(cls, v):
        if v and v not in zoneinfo.available_timezones():
            raise ValueError(f"The timezone '{v}' is unknown.")
        return v

    @root_validator(pre=False)
    def _check_coherence(cls, values):
        env = values.get("ENVIRONMENT")

        if env == Environment.PROD and "sqlite" in values.DB_URL.scheme:
            raise ValueError(
                f"You are trying to use sqlite in {values.ENVIRONMENT}, use a server based database instead."
            )

        if not values.get("USE_TZ") and values.get("TIMEZONE"):
            raise ValueError("Set 'USE_TZ' before attempting to use a timezone.")

        try:
            source = values["TORTOISE_ORM"]
            values["TORTOISE_ORM"] = cls.get_tortoise_orm(source, env)
        except (KeyError, OSError) as exp:
            raise ValueError("Cannot not load the database configuration.") from exp

        try:
            source = values["LOGGERS"]
            values["LOGGERS"] = cls.get_loggers(source)
        except (KeyError, OSError) as exp:
            raise ValueError("Cannot not load the loggers configuration.") from exp

        return values

    @classmethod
    def get_tortoise_orm(cls, source: PosixPath | dict, env) -> dict:
        if isinstance(source, PosixPath):
            with open(source, encoding="utf-8") as f:
                # SafeLoader ignore auxillary type so
                # ${}'s in config are loaded as that but we
                # don't want that.
                source = yaml.load(f, yaml.FullLoader)["config"]
        # FIXME: Write a parser for source
        tortoise_orm = source[env.value]
        # FIXME: Temporary solution, find a way
        # to cover all variables and type, by adding a parser
        # for example.
        if "use_tz" in tortoise_orm:
            tortoise_orm["use_tz"] = strtobool(tortoise_orm["use_tz"])
        return tortoise_orm

    @classmethod
    def get_loggers(cls, source: PosixPath | dict | dictConfigClass) -> dictConfigClass:
        if isinstance(source, dictConfigClass):
            return source

        if isinstance(source, PosixPath):
            with open(source, encoding="utf-8") as f:
                source = yaml.safe_load(f)["config"]
        try:
            return cls._validate_loggers(source)
        except (ValueError, TypeError, AttributeError, ImportError) as exp:
            raise ValueError("Cannot not load the loggers configuration.") from exp

    @classmethod
    def _validate_loggers(cls, source: dict):
        # call configure() later in app.setup()
        return dictConfigClass(source)


path_matcher = re.compile(r"\$\{([^}^{]+)\}")


def path_constructor(loader, node):
    """Extract the matched value, expand env variable, and replace the match"""

    value = node.value
    match = path_matcher.match(value)
    env_var = match.group()[2:-1]
    # return os.getenv(env_var) + value[match.end() :]
    return os.getenv(env_var)


def strtobool(word: str) -> bool:
    return word.lower() in {"true", "1", "t", "y", "yes"}
