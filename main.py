from fastapi import FastAPI
from config.db import engine
<<<<<<< HEAD
from routers import auth,admin
=======
from models import models
from routers import auth,admin,avocat
>>>>>>> e2659977dfb35671ee5a5fc4b1524769202225c5

app = FastAPI()
models.Base.metadata.create_all(engine)

app.include_router(auth.router)
app.include_router(admin.router)
<<<<<<< HEAD
=======
app.include_router(avocat.router)

>>>>>>> e2659977dfb35671ee5a5fc4b1524769202225c5

