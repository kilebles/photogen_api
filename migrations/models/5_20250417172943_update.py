from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "generations" ADD "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP;
        ALTER TABLE "generations" ADD "resolution" VARCHAR(50);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "generations" DROP COLUMN "updated_at";
        ALTER TABLE "generations" DROP COLUMN "resolution";"""
