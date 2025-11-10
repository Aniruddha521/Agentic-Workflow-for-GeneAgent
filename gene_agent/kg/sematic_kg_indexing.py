from sentence_transformers import SentenceTransformer
import faiss
import torch


class SematicKGIndexing:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.use_gpu = torch.cuda.is_available()
        self.gpu_device = torch.cuda.current_device() if self.use_gpu else None

        device = "cuda" if self.use_gpu else "cpu"
        self.model = SentenceTransformer(model_name, device=device)

        self.index = None
        self.embeddings = []
        self.docs = []

        # GPU resources for FAISS
        self.res = faiss.StandardGpuResources() if self.use_gpu else None

    def _create_index(self, dim):
        cpu_index = faiss.IndexFlatL2(dim)

        if self.use_gpu:
            print(f"[+] Using GPU device: {self.gpu_device}")
            gpu_index = faiss.index_cpu_to_gpu(self.res, self.gpu_device, cpu_index)
            return gpu_index

        print("[+] Using CPU index")
        return cpu_index

    def index_docs(self, docs: list):
        passages = [f"{d['node']} {d['relation']} {d['text']}" for d in docs]
        new_embeddings = (
            self.model.encode(passages, convert_to_numpy=True).astype("float32")
        )

        self.embeddings.append(new_embeddings)
        self.docs.extend(passages)

        if self.index is None:
            dim = new_embeddings.shape[1]
            self.index = self._create_index(dim)

        self.index.add(new_embeddings)
        return self.index

    def search(self, queries: list, top_k: int = 10):
        q = self.model.encode(queries, convert_to_numpy=True).astype("float32")
        faiss.normalize_L2(q)

        distances, indices = self.index.search(q, top_k)

        results = []
        for dist, idx in zip(distances[0], indices[0]):
            results.append((float(dist), self.docs[idx]))

        return results

    def range_search(self, queries: list, epsilon: float = 0.6):
        q_emb = self.model.encode(queries, convert_to_numpy=True).astype("float32")
        faiss.normalize_L2(q_emb)

        lims, D, I = self.index.range_search(q_emb, epsilon)
        results = []

        for qi in range(len(queries)):
            start = lims[qi]
            end = lims[qi + 1]
            for j in range(start, end):
                results.append(self.docs[I[j]])

        return results
