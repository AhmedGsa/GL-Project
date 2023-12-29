from fastapi import FastAPI, HTTPException, Request, status
from models import models
from config.db import engine
from routers import auth, search, appointment, rating, availabilities
from utils.jwt import JWT

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(search.router)
app.include_router(rating.router)
app.include_router(appointment.router)
app.include_router(availabilities.router)

@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    if request.url.path in ["/auth/login", "/auth/login/google", "/auth/redirect", "/auth/register-user"]:
        response = await call_next(request)
        return response
    token = request.headers.get("Authorization")
    token = token.split(" ")[1] if token else None
    print(token)
    if token:
        try:
            payload = JWT.verify_token(token)
            request.state.user = payload
        except:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    response = await call_next(request)
    return response

@app.get("/")
def read_root():
    return {"Hello": "chihab"}
