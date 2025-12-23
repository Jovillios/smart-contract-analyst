import shutil
import os

from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders import PyMuPDFLoader
from src.api.utils import extract_documents, ingest_documents, get_sources

app = FastAPI(title="Smart Contract Analyst")

class QueryRequest(BaseModel):
    question: str

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
vector_store = Chroma(
    collection_name="pdf_collection",
    embedding_function=embeddings,
    persist_directory="./chroma"
)
llm = ChatOpenAI(model="gpt-4o", temperature=0.0)

@app.post("/query")
def query_endpoint(request: QueryRequest):
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "Tu es un assistant spécialisé dans l'analyse de rapports financiers (URD)."),
        ("system", "Utilise UNIQUEMENT le contexte suivant. Contexte : {context}"),  
        ("user", "{question}")
    ])

    docs = vector_store.similarity_search(query=request.question, k=3)
    
    formatted_context = "\n\n".join([doc.page_content for doc in docs])

    chain = prompt_template | llm
    response = chain.invoke({
        "context": formatted_context,
        "question": request.question
    })
    print(docs)
    return {"answer": response.content, "sources": [get_sources(d.metadata) for d in docs]}


@app.post("/ingest")
def ingest_endpoint(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Seuls les fichiers PDF sont acceptés.")
    
    upload_dir = "./data/uploaded"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, file.filename)

    try:
        with open(file_path, "wb") as buffer:
            # copie le fichier uploadé vers le disque de manière efficiente
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la sauvegarde : {str(e)}")
    
    loader = PyMuPDFLoader(file_path)
    
    documents = extract_documents(loader)

    ingest_documents(vector_store, documents)

    return {
        "filename": file.filename,
        "total_pages": len(documents),
        "status": "Ingestion successful"
    }

@app.delete("/reset")
def reset_database():
    """Vide la base vectorielle (Utile pour le dev)."""
    try:
        vector_store.reset_collection() # Supprime tout
        # On doit recréer la collection après suppression si on veut continuer à l'utiliser
        # (Chroma gère ça parfois automatiquement, mais c'est plus sûr de ne pas crasher)
        return {"status": "Database cleared"}
    except Exception as e:
        # Souvent Chroma lève une erreur si la collection est vide, on l'attrape.
        return {"status": "Database was already empty or error", "detail": str(e)}