from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from deta import Deta
from .core import config

deta = Deta(config.settings.DETA_PROJECT_KEY)
db = deta.Base(config.settings.DETA_DB)

app = FastAPI(
    title=config.settings.PROJECT_NAME
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
    return {"messsage" : "Hello World!"}
