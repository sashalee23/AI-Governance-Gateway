from contextlib import asynccontextmanager
from fastapi import FastAPI

from .routes import router
from .db import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    init_db()
    yield
    # Shutdown (nothing to do yet, but this is where it would go)

app = FastAPI(title="AI Governed Gateway (MVP)", lifespan=lifespan)
app.include_router(router)