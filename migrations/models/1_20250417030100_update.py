from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "categories" RENAME COLUMN "name" TO "title";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "categories" RENAME COLUMN "title" TO "name";"""
