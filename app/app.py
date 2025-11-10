from fastapi import FastAPI
from pydantic import BaseModel
from contextlib import asynccontextmanager
from app.utils.get_retriever import get_retriever
from app.utils.doc_formatter import format_doc

retriever = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global retriever
    try:
        print("Loading Retriever...")
        retriever = get_retriever("app/chroma_shl_db_2")
        print("Retriever Loaded Successfully!")
    except Exception as e:
        print(f"Error loading retriever: {e}")
    yield
    retriever = None
    print("Retriever released.")

app = FastAPI(
    title="SHL Assessment Recommendation API",
    description="API that recommends SHL assessments based on user query",
    lifespan=lifespan
)

class QueryRequest(BaseModel):
    query: str

@app.get("/")
async def root():
    return {"message": "Welcome to SHL Assessment Recommendation API."}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/recommend")
async def recommend_assessments(request: QueryRequest):
    global retriever
    if retriever is None:
        print("Lazy-loading retriever...")
        retriever = get_retriever("app/chroma_shl_db_2")

    query = request.query
    print(f"Processing Query: {query}")

    docs = retriever.invoke(query)
    valid_docs = [
        doc for doc in docs
        if "url:" in doc.page_content and "name:" in doc.page_content
    ]

    if not valid_docs:
        return {"recommended_assessments": []}

    recommendations = [format_doc(doc) for doc in valid_docs[:10]]
    return {"recommended_assessments": recommendations}
