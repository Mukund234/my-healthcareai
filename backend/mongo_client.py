from typing import Optional

from pymongo import MongoClient

from config import settings

_mongo_client: Optional[MongoClient] = None


def get_mongo_client() -> Optional[MongoClient]:
    """
    Get a global MongoDB client if MONGO_URL is configured.
    Returns None if Mongo is not configured so the rest of the app can continue
    to work with the relational database only.
    """
    global _mongo_client

    if not settings.MONGO_URL:
        return None

    if _mongo_client is None:
        _mongo_client = MongoClient(settings.MONGO_URL)

    return _mongo_client


def get_mongo_db():
    """
    Convenience helper to get the configured MongoDB database.
    Returns None if Mongo is not configured.
    """
    client = get_mongo_client()
    if client is None:
        return None
    return client[settings.MONGO_DB_NAME]

