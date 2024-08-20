import mongoengine
from app.settings import settings

async def connect_db():
    mongoengine.connect(host=settings.MONGODB_URI)
    print("DB Connected")

async def disconnect_db():
    mongoengine.disconnect()
