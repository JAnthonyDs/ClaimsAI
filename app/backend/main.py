import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("Chave GROQ_API_KEY nao encontrada no .env")

app = FastAPI()

client = QdrantClient(url="http://localhost:6333")
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
vector_store = QdrantVectorStore(client=client, collection_name="claims_db", embedding=embeddings)

llm = ChatGroq(api_key=GROQ_API_KEY, temperature=0, model_name="llama-3.3-70b-versatile")

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vector_store.as_retriever(search_kwargs={"k": 3}),
    chain_type_kwargs={"prompt": PromptTemplate(
        template="Contexto: {context}\nPergunta: {question}\nResposta:",
        input_variables=["context", "question"]
    )}
)

class RequestBody(BaseModel):
    pergunta: str

@app.post("/api/chat")
def chat(body: RequestBody):
    try:
        response = qa_chain.invoke({"query": body.pergunta})
        return {"resposta": response['result']}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))