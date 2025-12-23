from typing import Sequence

from langchain_core.document_loaders.base import BaseLoader
from langchain_core.documents import Document
from langchain_core.vectorstores.base import VectorStore


def extract_documents(loader: BaseLoader) -> Sequence[Document]:
    docs = loader.load()
    return docs


def ingest_documents(vector_store: VectorStore, documents:  Sequence[Document]) -> None:
    vector_store.add_documents(documents=documents)