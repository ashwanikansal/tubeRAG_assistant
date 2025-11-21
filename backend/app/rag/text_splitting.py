from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

def get_default_text_splitter() -> RecursiveCharacterTextSplitter:
    """
    Returns a configured text splitter.
    """
    return RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
    )

def split_text_to_documents(text: str) -> List[Document]:
    """
    Splits raw transcript text into LangChain Document chunks.
    """
    print("Splitting transcript into chunks...")
    splitter = get_default_text_splitter()
    return splitter.create_documents([text])
