import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEndpoint,ChatHuggingFace

load_dotenv()

def get_llm(
    repo_id: str = "meta-llama/Meta-Llama-3-8B-Instruct",
    temperature: float = 0.1
):
    """
    Loads and returns a ready-to-use ChatHuggingFace LLM instance.
    """
    token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
    if not token:
        raise ValueError("HuggingFace API token not found in environment variables (.env).")

    model = HuggingFaceEndpoint(
        repo_id=repo_id,
        task="conversational",
        huggingfacehub_api_token=token,
        temperature=temperature
    )

    print(f" Loaded LLM: {repo_id}")
    return ChatHuggingFace(llm=model)
