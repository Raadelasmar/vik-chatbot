# VIK Chatbot - AI Engine Prototype

This is the core RAG (Retrieval-Augmented Generation) engine and FastAPI backend for the VIK Chatbot project.

## 🌟 Key Features
* **Smart Contextual Memory**: Unlike basic bots, this engine uses a "Query Rewriter" to look at chat history and fix pronouns (e.g., if a student asks "When is it?", the bot knows "it" refers to the exam mentioned earlier).
* **PDF-Aware Data Splitting**: The ingestion pipeline is custom-tuned for BME VIK documents, specifically recognizing subject codes like `BMEVI` and `BMEGT` to keep course info together.
* **Transparent RAG Pipeline**: Built using LangChain Expression Language (LCEL) for a clear, traceable flow from user input to final answer.
* **Dual Interface**: Includes a production-ready **FastAPI** backend and a **Streamlit** frontend for rapid testing and demos. 

## 🚀 Getting Started
1. **Clone & Environment**:
   - `git clone -b vik-chatbot-prototype https://github.com/Raadelasmar/vik-chatbot.git`
   - `cd vik-chatbot-prototype`
2. **Setup**:
   - Create a virtual environment: `python -m venv venv`
   - Install dependencies: `pip install -r requirements.txt`
3. **Configuration**:
   - Copy `.env.example` to a new file named `.env`.
   - Add your `GOOGLE_API_KEY` to the `.env` file.
4. **Data Ingestion**:
   - [cite_start]Place university PDFs in the `/data` folder. 
   - [cite_start]Run `python ingest_database.py` to build the local vector store. 
5. **Launch**:
   - [cite_start]Run the API: `fastapi dev main.py` 
   - [cite_start]Run the UI: `streamlit run ui.py`
