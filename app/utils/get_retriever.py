import os
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEndpointEmbeddings

load_dotenv()

def get_retriever(persist_directory: str):
    hf_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")

    embeddings = HuggingFaceEndpointEmbeddings(
        model="sentence-transformers/paraphrase-MiniLM-L3-v2",
        huggingfacehub_api_token=hf_token
    )

    vectordb = Chroma(
        persist_directory=persist_directory,
        embedding_function=embeddings
    )

    retriever = vectordb.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 10, "fetch_k": 30, "lambda_mult": 0.6}
    )

    print("Retriever initialized using Hugging Face Inference API")
    return retriever