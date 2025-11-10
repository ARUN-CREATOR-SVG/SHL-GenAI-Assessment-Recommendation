import os
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv

load_dotenv() 

def get_retriever(persist_directory: str):
    os.environ["HUGGINGFACEHUB_API_TOKEN"] = os.getenv("HUGGINGFACEHUB_API_TOKEN")

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectordb = Chroma(
        persist_directory=persist_directory,
        embedding_function=embeddings
    )

    retriever = vectordb.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 10, "fetch_k": 30, "lambda_mult": 0.6}
    )

    return retriever
