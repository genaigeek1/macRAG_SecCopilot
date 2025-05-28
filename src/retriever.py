
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

class VectorRetriever:
    def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        self.index = faiss.IndexFlatL2(384)
        self.texts = []

    def build_index(self, docs: list):
        self.texts = docs
        embeddings = self.model.encode(docs)
        self.index.add(np.array(embeddings, dtype='float32'))

    def query(self, q: str, k: int = 5):
        q_emb = self.model.encode([q])
        D, I = self.index.search(np.array(q_emb, dtype='float32'), k)
        return [self.texts[i] for i in I[0]]
