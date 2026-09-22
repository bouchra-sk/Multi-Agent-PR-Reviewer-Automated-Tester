from fastapi import FastAPI
from backend.app.api.codebase import router as codebase_router
from backend.app.api.onboarding import router as onboarding_router

app = FastAPI()

app.include_router(codebase_router)
app.include_router(onboarding_router)


@app.get("/")
def root():
    return {"message": "Backend is running"}