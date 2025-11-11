🧠 SHL GenAI Assessment Recommendation System

A Retrieval-Augmented Generation (RAG)–based AI system that recommends the most relevant SHL assessments for a given user query.
It combines web scraping, vector search, and LangChain-powered retrieval to provide smart, context-aware recommendations.

🚀 Features

✅ Web Scraping of SHL’s official product catalog (32 pages of “Individual Test Solutions”)
✅ Cleaned and structured data with detailed metadata like:

Assessment name

Test type (A/K/P/S)

Adaptive / Remote testing

Description, Duration, and Job levels

✅ RAG pipeline using:

LangChain + ChromaDB for vector storage

Hugging Face Embeddings for semantic search

✅ Evaluation using Recall@10 metric on labeled queries
✅ Optimized chunking and retriever logic to improve accuracy
✅ FastAPI backend + Streamlit frontend for easy interaction
✅ Render deployment with Hugging Face Inference API (no GPU or torch dependency)

🧩 Tech Stack
Category	Tools / Frameworks
Backend	FastAPI
Frontend	Streamlit
Vector Store	ChromaDB
Embeddings	Hugging Face Inference API (paraphrase-MiniLM-L3-v2)
Language Framework	LangChain
Deployment	Render (free tier)
Scraping	BeautifulSoup
Evaluation	Recall@10 metric
⚙️ System Architecture
User Query
   ↓
Hugging Face Inference API (Embeddings)
   ↓
Chroma Vector Database
   ↓
Retriever (MMR search)
   ↓
Recommended SHL Assessments

📊 Project Workflow
1️⃣ Web Scraping

Parsed the SHL Product Catalog using BeautifulSoup.

Filtered only “Individual Test Solutions.”

Extracted key fields (name, URL, test type, duration, etc.)

Saved clean dataset → data/shl_scraped_catalog.csv

2️⃣ Data Cleaning

Fixed /solutions/ URL mismatch between training data and scraped data.

Ensured all URLs are standardized for evaluation consistency.

3️⃣ RAG Setup

Converted records into LangChain Document objects.

Stored embeddings in ChromaDB.

Used MMR-based retriever for diverse, relevant results.

4️⃣ Model Optimization

Initial chunk size: 800 / 100 → Recall@10 = 0.293

Optimized chunk size: 1500 / 200 → Recall@10 = 0.433

Improved retrieval quality by increasing fetch_k to 30 and applying URL normalization.

5️⃣ Deployment

Backend API built in FastAPI (/recommend endpoint).

Streamlit app created for user queries and displaying ranked results.

Deployed on Render using Hugging Face’s hosted inference API to avoid OOM issues.

📈 Results Summary
Metric	Before	After
Chunk Size / Overlap	800 / 100	1500 / 200
Mean Recall@10	0.293	0.433
URL Consistency	Mismatched	✅ Fixed
Memory Usage	High (torch model)	✅ Optimized (HF API)
Runtime	Slow	✅ Stable on Render
🧠 Key Learnings

Importance of chunk size tuning in embedding-based retrieval

Using MMR retrieval to balance relevance and diversity

Handling data normalization issues (URL mismatches)

Optimizing model choice for low-memory environments like Render

Deploying end-to-end GenAI apps using LangChain + FastAPI + Hugging Face

🛠️ Setup Instructions
🔧 Prerequisites

Python 3.10 or 3.11

Hugging Face account (for API token)

📦 Installation
git clone https://github.com/ARUN-CREATOR-SVG/SHL-GenAI-Assessment-Recommendation.git
cd SHL-GenAI-Assessment-Recommendation
pip install -r requirements.txt

⚙️ Environment Variables

Create a .env file:

HUGGINGFACEHUB_API_TOKEN=hf_xxxxxxxxxxxxxxxxxxxxxx

▶️ Run Locally

Start FastAPI backend:

uvicorn app.app:app --reload


Run Streamlit frontend:

streamlit run streamlit_app.py

🌐 Deployment (Render)

Remove heavy dependencies (torch, sentence-transformers)

Use HuggingFaceHubEmbeddings for remote inference

Add your token in Render environment variables

Start command:

python -m uvicorn app.app:app --host 0.0.0.0 --port $PORT


🏁 Final Output

Fast and accurate recommendations for SHL assessments

Improved Recall@10 = 0.433

Deployed, scalable, and cost-free GenAI system

✨ Author

Arun Singh
💼 AI/ML & Data Science Enthusiast
🔗[ LinkedIn Profile](https://www.linkedin.com/in/arun-singh-7a7b9b289/)

📧[ arunsingh@example.com](arunsin2212@gmail.com)