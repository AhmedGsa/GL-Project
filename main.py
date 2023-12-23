from fastapi import FastAPI
from models import models
from config.db import engine
from routers import auth,admin

app = FastAPI()
models.Base.metadata.create_all(engine)

app.include_router(auth.router)
app.include_router(admin.router)

