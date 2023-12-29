from fastapi import FastAPI
from models import models
from config.db import engine
from routers import auth, search,rating

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(search.router)
app.include_router(rating.router)

@app.get("/")
def read_root():
    return {"Hello": "chihab"}
