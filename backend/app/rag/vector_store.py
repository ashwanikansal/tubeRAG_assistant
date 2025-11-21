from typing import Dict
from langchain_community.vectorstores import FAISS
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_core.documents import Document

from app.rag.embeddings import get_embeddings_model

# simple in-memory cache: video_id -> FAISS store
_VECTOR_STORES: Dict[str, FAISS] = {}


def build_vector_store_for_documents(docs: list[Document]) -> FAISS:
    """
    Builds a FAISS vector store from given documents using the shared embedding model.
    """
    embeddings = get_embeddings_model()
    vector_store = FAISS.from_documents(docs, embeddings)
    return vector_store


def get_or_create_vector_store(video_id: str, docs: list[Document]) -> FAISS:
    """
    Get a cached FAISS store if exists, otherwise build and cache it.
    """
    if video_id in _VECTOR_STORES:
        print("Vector store already exists.")
        return _VECTOR_STORES[video_id]

    print("Building vector store with embeddings...")
    vs = build_vector_store_for_documents(docs)
    _VECTOR_STORES[video_id] = vs
    return vs

def get_vector_store(video_id: str) -> FAISS:
    """
    Safe accessor so other modules don't touch _VECTOR_STORES directly.
    Raises KeyError if not present.
    """
    return _VECTOR_STORES[video_id]


def get_retriever(vector_store: FAISS, k: int = 5) -> VectorStoreRetriever:
    """
    Returns a retriever from FAISS with the given top-k.
    """
    retriever = vector_store.as_retriever(
        search_kwargs={"k": k},
    )
    return retriever
