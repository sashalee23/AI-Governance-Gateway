from fastapi import FastAPI
from .routes import router
from .db import init_db

app = FastAPI(title="AI Governance Gateway (Working title)")

@app.on_event("startup")
def _startup():
    init_db()

app.include_router(router)