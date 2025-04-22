from pathlib import Path
from fastapi.staticfiles import StaticFiles
import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from photogen_api.database.db import init_db
from photogen_api.routes import router
from photogen_api.config import config

MEDIA_ROOT = Path("media")

MEDIA_ROOT.mkdir(exist_ok=True)

app = FastAPI(title="Photogen API")

app.mount("/media", StaticFiles(directory=MEDIA_ROOT), name="media")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db(app)
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(
        "photogen_api.main:app",
        host=config.APP_HOST, 
        port=config.APP_PORT
    )
