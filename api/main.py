from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core import settings
from deta import Deta
from .routers import users_router

deta = Deta(settings.DETA_PROJECT_KEY)
db = deta.Base(settings.DETA_DB)

app = FastAPI(
    title=settings.PROJECT_NAME
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
async def root():
    db.put({
            "email": "lololol@example.com",
            "username": "Santi Esparrago",
            "password": "OhNoMyPwd3"
        })
    return {"messsage" : "User added"}

app.include_router(router=users_router.router)
