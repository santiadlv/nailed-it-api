from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from .core import settings
from .routers import users_router, salons_router, services_router, reservation_router, hours_router, reviews_router

app = FastAPI(title=settings.PROJECT_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.on_event('startup')
async def startup_db_client():
    app.mongodb_client = AsyncIOMotorClient(settings.MONGODB_URL)
    app.mongodb = app.mongodb_client[settings.MONGODB_NAME]

@app.on_event('shutdown')
async def shutdown_db_client():
    app.mongodb_client.close()

@app.get("/")
async def root():
    return {"messsage" : "Welcome!"}

app.include_router(router=users_router.router)
app.include_router(router=salons_router.router)
app.include_router(router=services_router.router)
app.include_router(router=reservation_router.router)
app.include_router(router=hours_router.router)
app.include_router(router=reviews_router.router)
