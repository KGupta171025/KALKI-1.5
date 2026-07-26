from typing import Optional, List, Dict, Any
from config.settings import settings

try:
    from qdrant_client import QdrantClient
    from qdrant_client.http import models as qmodels
    qdrant_client = QdrantClient(host=settings.QDRANT_HOST, port=settings.QDRANT_PORT)
except ImportError:
    qdrant_client = None
    qmodels = None

class QdrantConnectionManager:
    """
    Qdrant Connection Manager and Index Builder.
    """
    @staticmethod
    def get_client() -> Optional[Any]:
        return qdrant_client

    @staticmethod
    def create_collection_if_not_exists(collection_name: str, vector_size: int = 1536):
        if qdrant_client is not None and qmodels is not None:
            try:
                # Check if collection exists
                qdrant_client.get_collection(collection_name=collection_name)
            except Exception:
                # Create collection with Cosine distance indexing configuration
                qdrant_client.create_collection(
                    collection_name=collection_name,
                    vectors_config=qmodels.VectorParams(
                        size=vector_size,
                        distance=qmodels.Distance.COSINE
                    )
                )
                print(f"[Qdrant] Collection '{collection_name}' created successfully.")
            return True
        print(f"[Qdrant MOCK] Skip collection creation. Qdrant driver offline.")
        return False

    @staticmethod
    def check_health() -> Dict[str, Any]:
        if qdrant_client is not None:
            try:
                # Retrieve cluster health info
                collections = qdrant_client.get_collections()
                return {
                    "status": "CONNECTED",
                    "collections_count": len(collections.collections)
                }
            except Exception as e:
                return {"status": "UNREACHABLE", "error": str(e)}
        return {"status": "MOCK_CONNECTED", "collections_count": 2}

qdrant_manager = QdrantConnectionManager()
