import re
from typing import List, Dict, Any, Optional

class SemanticChunker:
    """
    Decomposes raw documents into semantic text passages with sliding overlaps
    and inherits document-level metadata.
    """
    @staticmethod
    def chunk_document(
        text: str, 
        chunk_size: int = 512, 
        overlap: int = 64,
        metadata: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        meta = metadata or {}
        
        # Simple regex split by sentence boundaries to preserve semantics
        sentences = re.split(r'(?<=[.!?])\s+', text)
        chunks = []
        current_chunk = []
        current_length = 0

        for sentence in sentences:
            sentence_len = len(sentence.split())
            if current_length + sentence_len > chunk_size:
                # Compile chunk
                chunk_text = " ".join(current_chunk)
                chunks.append({
                    "content": chunk_text,
                    "length": len(chunk_text),
                    "metadata": {
                        **meta,
                        "chunk_index": len(chunks)
                    }
                })
                
                # Apply sliding overlap window
                overlap_words = current_chunk[-overlap:] if len(current_chunk) >= overlap else current_chunk
                current_chunk = list(overlap_words)
                current_length = sum(len(w.split()) for w in current_chunk)

            current_chunk.append(sentence)
            current_length += sentence_len

        # Flush final remaining segment
        if current_chunk:
            chunk_text = " ".join(current_chunk)
            chunks.append({
                "content": chunk_text,
                "length": len(chunk_text),
                "metadata": {
                    **meta,
                    "chunk_index": len(chunks)
                }
            })

        return chunks

semantic_chunker = SemanticChunker()
