from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


def get_retriever(persist_directory: str):
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    vectordb = Chroma(
        persist_directory=persist_directory,
        embedding_function=embedding_model
    )
    
    retriever = vectordb.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": 10,
            "fetch_k": 30,
            "lambda_mult": 0.6,
            "score_threshold": 0.3
        }
    )
    
    return retriever