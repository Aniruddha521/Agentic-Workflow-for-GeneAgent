from sentence_transformers import SentenceTransformer
import faiss
import torch
import numpy as np


class SematicKGIndexing:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        # GPU only for embedding model (safe)
        self.use_gpu = torch.cuda.is_available()
        device = "cuda" if self.use_gpu else "cpu"

        self.model = SentenceTransformer(model_name, device=device)

        # FAISS index always on CPU (GPU Flat does NOT support range_search)
        self.index = None
        self.docs = []
        self.embeddings = None  # numpy array

    def _create_index(self, dim: int):
        print("[+] Creating CPU IndexFlatL2 (supports range_search)")
        index = faiss.IndexFlatL2(dim)  # cosine similarity via normalized L2
        return index

    def index_docs(self, docs: list):
        passages = [f"{d['node']} {d['relation']} {d['text']}" for d in docs]

        # Encode embeddings (GPU OR CPU depending on system)
        new_emb = self.model.encode(passages, convert_to_numpy=True)
        new_emb = new_emb.astype("float32")

        # Normalize for cosine similarity
        faiss.normalize_L2(new_emb)

        if self.embeddings is None:
            self.embeddings = new_emb
        else:
            self.embeddings = np.vstack([self.embeddings, new_emb])

        self.docs.extend(passages)

        # Create FAISS index if first time
        if self.index is None:
            dim = new_emb.shape[1]
            self.index = self._create_index(dim)

        # Add to FAISS
        self.index.add(new_emb)
        return self.index

    def search(self, queries: list, top_k: int = 10):
        q = self.model.encode(queries, convert_to_numpy=True).astype("float32")
        faiss.normalize_L2(q)

        # Standard KNN search
        distances, indices = self.index.search(q, top_k)

        results = []
        for idx in indices[0]:
            if idx < len(self.docs):
                results.append(self.docs[idx])

        return results

    def range_search(self, queries: list, epsilon: float = 0.6):
        q_emb = self.model.encode(queries, convert_to_numpy=True).astype("float32")
        faiss.normalize_L2(q_emb)

        # Must be 2D
        if q_emb.ndim == 1:
            q_emb = q_emb.reshape(1, -1)

        lims, D, I = self.index.range_search(q_emb, epsilon)

        results = []
        for qi in range(len(queries)):
            start = lims[qi]
            end = lims[qi + 1]
            for j in range(start, end):
                idx = I[j]
                if idx < len(self.docs):
                    results.append(self.docs[idx])

        return results
