from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "categories" ADD "gender" VARCHAR(10);
        ALTER TABLE "categories" ADD "position" INT NOT NULL DEFAULT 0;
        ALTER TABLE "categories" ADD "prompt" TEXT;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "categories" DROP COLUMN "gender";
        ALTER TABLE "categories" DROP COLUMN "position";
        ALTER TABLE "categories" DROP COLUMN "prompt";"""
