import re
from typing import List, Tuple
from app.indexer import CorpusIndex, DocumentChunk

class Retriever:
    def __init__(self, index: CorpusIndex):
        self.index = index

    def retrieve(
        self,
        query: str,
        top_k: int = 6,
        customer_facing: bool = True
    ) -> List[DocumentChunk]:
        if not self.index.bm25 or not self.index.chunks:
            return []

        tokens = CorpusIndex.tokenize(query)
        if not tokens:
            return []

        raw_scores = self.index.bm25.get_scores(tokens)
        scored_chunks: List[Tuple[float, DocumentChunk]] = []

        is_asking_historical = any(w in query.lower() for w in ["2024", "historical", "previous", "grandfathered", "old"])

        for score, chunk in zip(raw_scores, self.index.chunks):
            # Strict confidentiality filter
            if customer_facing:
                if chunk.audience.lower() == "internal":
                    continue
                if chunk.status.lower() == "draft":
                    continue

            # Check supersession
            if chunk.status.lower() == "superseded" and not is_asking_historical:
                # Downweight superseded documents heavily so current docs prevail
                score = score * 0.15

            # Authority weighting
            # authority is between 20 (forum) and 100 (refund policy/terms of service)
            authority_multiplier = 0.8 + (chunk.authority / 250.0) # range ~ 0.88 to 1.2
            final_score = score * authority_multiplier

            # Title / Header exact phrase boost
            q_lower = query.lower()
            if any(term in chunk.doc_title.lower() for term in tokens):
                final_score += 1.5
            if any(term in chunk.section_title.lower() for term in tokens):
                final_score += 1.0

            if final_score > 0.05:
                scored_chunks.append((final_score, chunk))

        scored_chunks.sort(key=lambda x: x[0], reverse=True)
        return [c for _, c in scored_chunks[:top_k]]
