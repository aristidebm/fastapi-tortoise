import enum

from pydantic import AnyUrl


class PatronStatus(enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    BLOCKED = "blocked"


class BookLendingReturnStatus(enum.Enum):
    GOOD = "good"
    DAMAGED = "damaged"


class Environment(enum.Enum):
    TEST = "test"
    DEV = "development"
    STAGE = "staging"
    PROD = "production"


class SQLiteDsn(AnyUrl):
    __slots__ = ()
    allowed_schemes = {
        "sqlite",
        "sqlite3",
        "sqlite+aiosqlite",
        "sqlite3+aiosqlite",
    }
    host_required = False
