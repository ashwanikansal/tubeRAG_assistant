from functools import lru_cache
from langchain_huggingface import HuggingFaceEmbeddings

@lru_cache(maxsize=1)
def get_embeddings_model() -> HuggingFaceEmbeddings:
    """
    Returns a singleton embedding model instance.
    """
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-mpnet-base-v2"
    )
