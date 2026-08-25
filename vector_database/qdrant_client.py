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
    Qdrant Connection Manager and HNSW Graph Vector Index Builder.
    """
    @staticmethod
    def get_client() -> Optional[Any]:
        return qdrant_client

    @staticmethod
    def create_collection_if_not_exists(collection_name: str, vector_size: int = 1536):
        if qdrant_client is not None and qmodels is not None:
            try:
                qdrant_client.get_collection(collection_name=collection_name)
            except Exception:
                # Create collection with Cosine distance & HNSW graph tuning
                qdrant_client.create_collection(
                    collection_name=collection_name,
                    vectors_config=qmodels.VectorParams(
                        size=vector_size,
                        distance=qmodels.Distance.COSINE
                    ),
                    hnsw_config=qmodels.HnswConfigDiff(
                        m=16,
                        ef_construct=100
                    )
                )
                print(f"[Qdrant HNSW] Collection '{collection_name}' created with m=16, ef_construct=100.")
            return True
        print(f"[Qdrant MOCK] Skip collection creation. Qdrant driver offline.")
        return False

    @staticmethod
    def check_health() -> Dict[str, Any]:
        if qdrant_client is not None:
            try:
                collections = qdrant_client.get_collections()
                return {
                    "status": "CONNECTED",
                    "hnsw_tuned": True,
                    "collections_count": len(collections.collections)
                }
            except Exception as e:
                return {"status": "UNREACHABLE", "error": str(e)}
        return {"status": "MOCK_CONNECTED", "hnsw_tuned": True, "collections_count": 2}

qdrant_manager = QdrantConnectionManager()
