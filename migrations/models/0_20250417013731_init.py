from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "categories" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(100) NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS "styles" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(100) NOT NULL UNIQUE,
    "category_id" INT NOT NULL REFERENCES "categories" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "users" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "telegram_id" VARCHAR(100) NOT NULL UNIQUE,
    "first_name" VARCHAR(100),
    "last_name" VARCHAR(100),
    "username" VARCHAR(100),
    "role" VARCHAR(50) NOT NULL DEFAULT 'new',
    "gender" VARCHAR(10),
    "tokens" INT NOT NULL DEFAULT 0,
    "photo" VARCHAR(255),
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS "user_jobs" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "job_id" VARCHAR(100) NOT NULL,
    "job_type" VARCHAR(50) NOT NULL,
    "status" VARCHAR(50) NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "user_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "generations" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "image_url" VARCHAR(255) NOT NULL,
    "prompt" TEXT NOT NULL,
    "status" VARCHAR(50) NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "category_id" INT NOT NULL REFERENCES "categories" ("id") ON DELETE CASCADE,
    "job_id" INT REFERENCES "user_jobs" ("id") ON DELETE CASCADE,
    "style_id" INT REFERENCES "styles" ("id") ON DELETE CASCADE,
    "user_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "user_profiles" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "lora_id" VARCHAR(100),
    "status" VARCHAR(50),
    "job_id" INT,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "user_id" INT NOT NULL UNIQUE REFERENCES "users" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
