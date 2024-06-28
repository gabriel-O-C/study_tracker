from fastapi import FastAPI

from .subjects.router import router as subjects_router

app = FastAPI()

app.include_router(subjects_router)
