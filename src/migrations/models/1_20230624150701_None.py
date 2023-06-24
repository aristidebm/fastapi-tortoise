from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "todos" (
    "id" CHAR(36) NOT NULL  PRIMARY KEY,
    "created" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "title" VARCHAR(255) NOT NULL,
    "description" TEXT,
    "status" VARCHAR(255) NOT NULL  DEFAULT 'created' /* CREATED: created\nINPROGRESS: inProgress\nDONE: done */
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSON NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
