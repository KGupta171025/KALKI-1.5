from typing import List, Dict, Any
from database.neo4j_driver import graph_db

class KnowledgeGraphRetriever:
    """
    Queries Neo4j knowledge graphs to retrieve entity relations (triples).
    """
    @staticmethod
    async def get_entity_context(entities: List[str]) -> List[Dict[str, Any]]:
        if not entities:
            return []

        # Find paths matching query entities
        query = """
        MATCH (s)-[r]->(o)
        WHERE s.name IN $entity_names OR o.name IN $entity_names
        RETURN s.name as subject, type(r) as predicate, o.name as object
        LIMIT 10
        """
        try:
            records = await graph_db.run_query(query, {"entity_names": entities})
            return records
        except Exception as e:
            print(f"[RAG Graph] Failed to query graph DB: {str(e)}")
            return []

graph_retriever = KnowledgeGraphRetriever()
