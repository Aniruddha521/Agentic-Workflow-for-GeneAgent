from typing import List, Tuple, Dict
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
import heapq
from dataclasses import dataclass
from .inmemory_kg import InMemoryKG

@dataclass
class SemanticKGIndex:
    kg: InMemoryKG
    model_name: str = "all-MiniLM-L6-v2"
    model: SentenceTransformer = None
    index: faiss.IndexFlatIP = None
    triple_texts: List[str] = None

    def __post_init__(self):
        self.model = SentenceTransformer(self.model_name)
        self.triple_texts = []
        self.index = None

    def build_index(self):
        triples = self.kg.export_triples()
        self.triple_texts = [f"{s} {p} {o}" for s, p, o in triples]
        if not self.triple_texts:
            print("No triples to index.")
            return
        embeddings = self.model.encode(self.triple_texts, convert_to_numpy=True, show_progress_bar=False)
        # normalize for cosine-similarity with inner product
        faiss.normalize_L2(embeddings)
        dim = embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dim)
        self.index.add(embeddings)
        print(f"Built FAISS index with {len(self.triple_texts)} items (dim={dim}).")

    def query(self, question: str, top_k: int = 8) -> List[Tuple[float, str, Tuple[str, str, str]]]:
        """Return list of (score, triple_text, triple_tuple)"""
        if self.index is None:
            raise RuntimeError("Index not built. Call build_index() first.")
        q_emb = self.model.encode([question], convert_to_numpy=True)
        faiss.normalize_L2(q_emb)
        D, I = self.index.search(q_emb, top_k)
        results = []
        all_triples = self.kg.export_triples()
        for score, idx in zip(D[0], I[0]):
            if idx < 0 or idx >= len(self.triple_texts):
                continue
            tri_text = self.triple_texts[idx]
            tri_tuple = all_triples[idx]
            results.append((float(score), tri_text, tri_tuple))
        return results

