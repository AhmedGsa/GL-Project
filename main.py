from fastapi import FastAPI
from models import models
from config.db import engine
from routers import auth

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)

@app.get("/")
def read_root():
    return {"Hello": "chihab"}
