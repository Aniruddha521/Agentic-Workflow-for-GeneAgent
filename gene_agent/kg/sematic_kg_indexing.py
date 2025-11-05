from sentence_transformers import SentenceTransformer
import numpy as np
import faiss


class SematicKGIndexing:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.embeddings = []
        self.docs = []

    def index_docs(self, docs: list):
        passages = [f"{d['node']} {d['relation']} {d['text']}" for d in docs]
        new_embeddings = self.model.encode(passages, convert_to_numpy=True)
        self.embeddings.append(new_embeddings)
        self.docs.extend(passages)

        if self.index is None:
            dimension = new_embeddings.shape[1]
            self.index = faiss.IndexFlatL2(dimension)

        self.index.add(new_embeddings)

        return self.index

    def search(self, queries: list, top_k: int = 10):
        query_embedding = self.model.encode(queries, convert_to_numpy=True)
        faiss.normalize_L2(query_embedding)
        distances, indices = self.index.search(query_embedding, top_k)

        results = []
        for dist, idx in zip(distances[0], indices[0]):
            results.append((dist, self.docs[idx]))

        return results
    
    def range_search(self, queries: list, epsilon: float = 0.6):
        q_emb = self.model.encode(queries, convert_to_numpy=True)
        faiss.normalize_L2(q_emb)
        lims, D, I = self.index.range_search(q_emb, epsilon)
        results = []

        for qi in range(len(queries)):
            start = lims[qi]
            end = lims[qi + 1]

            # hits = []
            for j in range(start, end):
                # hits.append({
                #     "text": self.docs[I[j]],
                #     "score": float(D[j]),
                #     "idx": int(I[j])
                # })
                results.append(self.docs[I[j]])

        return results
