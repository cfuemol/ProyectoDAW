import mongoengine
import os

def init_mongo():
    mongoengine.connect(
        db=os.environ.get("MONGO_DB"),
        host=os.environ.get("MONGO_HOST"),
        port=int(os.environ.get("MONGO_PORT")),
        username=os.environ.get("MONGO_USER"),
        password=os.environ.get("MONGO_PASS"),
        authentication_source="admin",
    )