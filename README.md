# VIK Chatbot - AI Engine Prototype

[cite_start]This is the core RAG (Retrieval-Augmented Generation) engine and FastAPI backend for the VIK Chatbot project.

## 🛠️ Features
- **FastAPI Backend**: Clean REST API for question-answering. 
-**RAG Pipeline**: Document retrieval using LangChain and ChromaDB. 
- **Query Rewriting**: Intelligent context handling for chat history. 
- **Streamlit UI**: A built-in testing interface. 

## 🚀 Getting Started
1. **Clone & Environment**:
   - `git clone https://github.com/gdg-oc-bme/vik-chatbot.git`
   - `cd vik-chatbot-prototype`
2. **Setup**:
   - Create a virtual environment: `python -m venv venv`
   - Install dependencies: `pip install -r requirements.txt`
3. **Configuration**:
   - Copy `.env.example` to a new file named `.env`.
   - Add your `GOOGLE_API_KEY` to the `.env` file.
4. **Data Ingestion**:
   - [cite_start]Place university PDFs in the `/data` folder. [cite: 8]
   - [cite_start]Run `python ingest_database.py` to build the local vector store. [cite: 21]
5. **Launch**:
   - [cite_start]Run the API: `fastapi dev main.py` [cite: 25]
   - [cite_start]Run the UI: `streamlit run ui.py`
