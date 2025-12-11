import os
import re
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings 
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http import models

load_dotenv()

PDF_PATH = "../data/apolice.pdf"
COLLECTION_NAME = "claims_db"
QDRANT_URL = "http://localhost:6333"
MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

def run_ingestion():
    embeddings_model = HuggingFaceEmbeddings(model_name=MODEL_NAME)

    loader = PyPDFLoader(PDF_PATH)
    raw_documents = loader.load()

    full_text = ""
    for doc in raw_documents:
        # Junta todas as páginas num textão só limpo
        full_text += re.sub(r'\s+', ' ', doc.page_content).strip() + " "

    print(f"Texto total extraído: {len(full_text)} caracteres.")

    #Cortando texto (Recursive Splitter)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    
    chunks = text_splitter.create_documents([full_text])
    print(f"   -> Gerados {len(chunks)} blocos garantidos.")

    #Salvar
    client = QdrantClient(url=QDRANT_URL)
    
    if client.collection_exists(COLLECTION_NAME):
        client.delete_collection(COLLECTION_NAME)
    
    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=models.VectorParams(size=384, distance=models.Distance.COSINE),
    )
    QdrantVectorStore.from_documents(
        chunks,
        embeddings_model,
        url=QDRANT_URL,
        collection_name=COLLECTION_NAME,
        force_recreate=False
    )

if __name__ == "__main__":
    run_ingestion()