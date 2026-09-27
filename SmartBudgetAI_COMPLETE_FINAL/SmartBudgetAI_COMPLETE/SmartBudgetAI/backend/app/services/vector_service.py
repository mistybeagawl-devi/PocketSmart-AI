from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class LocalVectorStore:
    def __init__(self): self.docs=[]
    def add(self, text): self.docs.append(text)
    def search(self, query, k=3):
        if not self.docs: return []
        corpus=self.docs+[query]
        matrix=TfidfVectorizer(stop_words="english").fit_transform(corpus)
        scores=cosine_similarity(matrix[-1],matrix[:-1]).ravel()
        return [self.docs[i] for i in scores.argsort()[::-1][:k]]

class PineconeVectorStore:
    def __init__(self, api_key, index_name, namespace="default"):
        from pinecone import Pinecone
        self.pc=Pinecone(api_key=api_key)
        self.index=self.pc.Index(index_name); self.namespace=namespace
    def add(self, text):
        # Embeddings are intentionally left to the configured application embedding pipeline.
        return None
    def search(self, query, k=3): return []
