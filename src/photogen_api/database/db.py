from tortoise.contrib.fastapi import register_tortoise

from photogen_api.config import config


def init_db(app):
    register_tortoise(
        app,
        db_url=config.DATABASE_URL,
        modules={"models": ["photogen_api.database.models"]},
        generate_schemas=False,
        add_exception_handlers=True,
    )