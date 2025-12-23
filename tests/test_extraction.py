from src.api.utils import extract_documents
from langchain_community.document_loaders import PyMuPDFLoader, PyPDFLoader

def test_extract_documents():
    pdf_path = "./data/pdf/LVMH-55-67.pdf"
    pymupdf_loader = PyMuPDFLoader(pdf_path) 
    pypdf_loader = PyPDFLoader(pdf_path)

    assert len(extract_documents(pymupdf_loader)) == 13
    assert len(extract_documents(pypdf_loader)) == 13