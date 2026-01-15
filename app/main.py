from fastapi import FastAPI
from .routes import router

app = FastAPI(title="AI Governance Gateway (Working title)")
app.include_router(router)