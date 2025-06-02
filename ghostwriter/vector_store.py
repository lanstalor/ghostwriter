"""Simple in-memory vector store for embeddings."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

import numpy as np

try:
    import openai
except ImportError:  # pragma: no cover - optional dependency
    openai = None


def _embed_text(text: str) -> np.ndarray:
    """Return embedding for given text using OpenAI embeddings API."""
    if openai is None:
        raise ImportError("openai package is required for embeddings")
    response = openai.Embedding.create(model="text-embedding-ada-002", input=text)
    vec = response["data"][0]["embedding"]
    return np.array(vec, dtype=np.float32)


@dataclass
class VectorStore:
    """Stores embeddings and the original texts."""

    texts: List[str] = field(default_factory=list)
    embeddings: List[np.ndarray] = field(default_factory=list)

    def add_texts(self, texts: List[str]) -> None:
        """Embed and store multiple texts."""
        for text in texts:
            self.texts.append(text)
            self.embeddings.append(_embed_text(text))

    def query_similar(self, text: str, k: int = 5) -> List[str]:
        """Return the top-k most similar stored passages."""
        if not self.embeddings:
            return []
        query_vec = _embed_text(text)
        matrix = np.vstack(self.embeddings)
        # cosine similarity
        sims = matrix @ query_vec / (
            np.linalg.norm(matrix, axis=1) * np.linalg.norm(query_vec) + 1e-9
        )
        indices = np.argsort(-sims)[:k]
        return [self.texts[i] for i in indices]
