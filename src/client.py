from motor.motor_asyncio import AsyncIOMotorClient
from .config import settings

clinet = AsyncIOMotorClient(
    settings.MONGO_URI,
    tlsCAFile = None,
    tlsAllowInvalidCertificates = True
)

db = clinet[settings.DATABASE_NAME]

messages_collection = db["messages"]
summaries_collection = db["summaries"]