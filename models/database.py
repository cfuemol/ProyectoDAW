import os
from mongoengine import connect
from dotenv import load_dotenv

load_dotenv()

def init_db():
    connect(
        db=os.getenv("MONGO_DB"),
        host=f"mongodb://{os.getenv('MONGO_USER')}:{os.getenv('MONGO_PASSWORD')}@{os.getenv('MONGO_HOST')}:27017/{os.getenv('MONGO_DB')}?authSource=admin"
    )
