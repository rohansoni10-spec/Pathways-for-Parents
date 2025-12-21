from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure
from config import settings
import certifi

# Global MongoDB client instance
mongodb_client: AsyncIOMotorClient | None = None


async def connect_to_mongodb() -> None:
    """
    Connect to MongoDB Atlas using Motor async client.
    Called on application startup.
    """
    global mongodb_client
    
    try:
        # Debug: Print URI format (without exposing credentials)
        uri = settings.mongodb_uri
        if uri:
            uri_prefix = uri.split('://')[0] if '://' in uri else 'NO_SCHEME'
            print(f"DEBUG: MongoDB URI scheme: {uri_prefix}")
            print(f"DEBUG: URI length: {len(uri)}")
        else:
            print("ERROR: MONGODB_URI is empty or None")
            raise ValueError("MONGODB_URI environment variable is not set")
        
        mongodb_client = AsyncIOMotorClient(
            settings.mongodb_uri,
            serverSelectionTimeoutMS=5000,
            tlsCAFile=certifi.where()
        )
        # Verify connection
        await mongodb_client.admin.command("ping")
        print("✓ Successfully connected to MongoDB Atlas")
    except ConnectionFailure as e:
        print(f"✗ Failed to connect to MongoDB: {e}")
        raise
    except Exception as e:
        print(f"✗ Unexpected error connecting to MongoDB: {e}")
        raise


async def close_mongodb_connection() -> None:
    """
    Close MongoDB connection.
    Called on application shutdown.
    """
    global mongodb_client
    
    if mongodb_client:
        mongodb_client.close()
        print("✓ MongoDB connection closed")


def get_database():
    """
    Get the MongoDB database instance.
    Returns the database specified in the connection URI.
    """
    if mongodb_client is None:
        raise RuntimeError("Database not initialized. Call connect_to_mongodb() first.")
    
    # Extract database name from URI or use default
    return mongodb_client.get_default_database()


async def ping_database() -> bool:
    """
    Ping the database to check connection health.
    Returns True if connection is healthy, False otherwise.
    """
    try:
        if mongodb_client is None:
            return False
        
        await mongodb_client.admin.command("ping")
        return True
    except Exception:
        return False