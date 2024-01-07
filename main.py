from fastapi import FastAPI
from models import models

from config.db import engine
from routers import auth,admin
import json
from config.db import engine
from routers import auth,admin
from models import models
from routers import auth,admin,avocat

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(avocat.router)

