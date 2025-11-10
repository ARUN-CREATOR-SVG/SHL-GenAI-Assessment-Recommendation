from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from contextlib import asynccontextmanager
from app.utils.get_retriever import get_retriever
from app.utils.doc_formatter import format_doc

retriever = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global retriever
    try:
        print("Loading retriever...")
        retriever = get_retriever("app/chroma_shl_db_2")
        print("Retriever loaded successfully!")
    except Exception as e:
        print(f"Failed to load retriever: {e}")
    
    yield
    

    print("Shutting down...")

app = FastAPI(
    title="SHL Assessment Recommendation API",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],         
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str

@app.get("/")
async def root():
    return {"message": "API is running"}

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "retriever_loaded": retriever is not None
    }

@app.post("/recommend")
async def recommend(request: QueryRequest):
    if retriever is None:
        return {"error": "Retriever not loaded yet."}

    try:
        docs = retriever.invoke(request.query)
        valid_docs = [
            doc for doc in docs
            if "url:" in doc.page_content and "name:" in doc.page_content
        ]

        if not valid_docs:
            return {"recommended_assessments": []}

        recommendations = [format_doc(doc) for doc in valid_docs[:10]]
        return {"recommended_assessments": recommendations}

    except Exception as e:
        print("Error while processing query:", e)
        return {"error": "Failed to process query", "details": str(e)}