from fastapi import FastAPI
from config.db import engine
from models import models
from routers import auth,admin,avocat

app = FastAPI()
models.Base.metadata.create_all(engine)

app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(avocat.router)


