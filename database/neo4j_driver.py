from typing import Optional, List, Dict, Any
from config.settings import settings

try:
    from neo4j import AsyncGraphDriver, GraphDatabase
    neo4j_driver = GraphDatabase.driver(
        settings.NEO4J_URI,
        auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD)
    )
except ImportError:
    neo4j_driver = None

class Neo4jDriverManager:
    """
    Manages Graph DB driver connections and executes queries.
    """
    @staticmethod
    async def run_query(query: str, parameters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        if neo4j_driver is not None:
            async with neo4j_driver.session() as session:
                result = await session.run(query, parameters or {})
                records = await result.data()
                return records
        
        # Mock Graph Database Fallback
        print(f"[Neo4j MOCK] Executed query: '{query}'")
        return [{"subject": "KALKI", "predicate": "isA", "object": "IntelligenceOperatingSystem"}]

    @staticmethod
    async def close():
        if neo4j_driver is not None:
            await neo4j_driver.close()

graph_db = Neo4jDriverManager()
