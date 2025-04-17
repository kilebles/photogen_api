from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "styles" DROP CONSTRAINT IF EXISTS "fk_styles_categori_78c31f1c";
        ALTER TABLE "styles" ADD "prompt" TEXT NOT NULL;
        ALTER TABLE "styles" RENAME COLUMN "name" TO "title";
        ALTER TABLE "styles" RENAME COLUMN "category_id" TO "position";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "styles" RENAME COLUMN "title" TO "name";
        ALTER TABLE "styles" RENAME COLUMN "position" TO "category_id";
        ALTER TABLE "styles" DROP COLUMN "prompt";
        ALTER TABLE "styles" ADD CONSTRAINT "fk_styles_categori_78c31f1c" FOREIGN KEY ("category_id") REFERENCES "categories" ("id") ON DELETE CASCADE;"""
