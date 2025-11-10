from fastapi import FastAPI
from pydantic import BaseModel
from app.utils.get_retriever import get_retriever
from app.utils.doc_formatter import format_doc
import gc

app = FastAPI(
    title="SHL Assessment Recommendation API",
    description="API that recommends SHL assessments based on user query"
)

retriever = None

class QueryRequest(BaseModel):
    query: str

@app.on_event("startup")
async def startup_event():
    """Don't load retriever at startup - save memory"""
    print("API Started - Retriever will load on first request")

@app.get("/")
async def root():
    return {"message": "Welcome to SHL Assessment Recommendation API."}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "retriever_loaded": retriever is not None}

@app.post("/recommend")
async def recommend_assessments(request: QueryRequest):
    global retriever
  
    if retriever is None:
        print("🔄 Loading retriever on first request...")
        try:
            retriever = get_retriever("app/chroma_shl_db_2")
            gc.collect()
            print("✅ Retriever loaded successfully")
        except Exception as e:
            print(f" Error loading retriever: {e}")
            return {"error": "Failed to load retriever", "details": str(e)}

    query = request.query
    print(f"🔍 Processing Query: {query}")

    try:
        docs = retriever.invoke(query)
        valid_docs = [
            doc for doc in docs
            if "url:" in doc.page_content and "name:" in doc.page_content
        ]

        if not valid_docs:
            return {"recommended_assessments": []}

        recommendations = [format_doc(doc) for doc in valid_docs[:10]]
        return {"recommended_assessments": recommendations}
    
    except Exception as e:
        print(f" Error processing query: {e}")
        return {"error": "Failed to process query", "details": str(e)}