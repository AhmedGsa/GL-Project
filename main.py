from fastapi import FastAPI
from models import models
from config.db import engine

app = FastAPI()
models.Base.metadata.create_all(engine)

@app.get("/")
def read_root():
    return {"Hello": "chihab"}
