import os
from typing import Sequence, Dict

from langchain_core.document_loaders.base import BaseLoader
from langchain_core.documents import Document
from langchain_core.vectorstores.base import VectorStore


def extract_documents(loader: BaseLoader) -> Sequence[Document]:
    docs = loader.load()
    return docs


def ingest_documents(vector_store: VectorStore, documents:  Sequence[Document]) -> None:
    vector_store.add_documents(documents=documents)


def get_sources(metadata: Dict[str, str]) -> Dict[str, str]:
    page = metadata["page"]
    source = os.path.basename(metadata["file_path"])
    return { "source": source, "page": page}