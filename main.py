from fastapi import FastAPI
from pydantic import BaseModel
import os
from dotenv import load_dotenv

# No more confusing black-box wrappers! Just pure LCEL tools.
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

load_dotenv()
app = FastAPI(title="VIK University Assistant API")

# 1. Setup Database & LLM
embeddings_model = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
vector_store = Chroma(
    collection_name="vik_collection", 
    embedding_function=embeddings_model, 
    persist_directory="chroma_db"
)
retriever = vector_store.as_retriever(search_kwargs={'k': 8})
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", version="v1", temperature=0.2)

# --- 2. THE TRANSPARENT ARCHITECTURE ---

# Step A: The Rewriter
rewrite_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert question re-writer. Look at the chat history and the user's new question. "
               "If the new question uses pronouns or refers to a previous topic, rewrite it to explicitly "
               "include the specific subject from the history. If no rewrite is needed, repeat the exact question. "
               "ONLY output the rewritten question."),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}")
])

# Step B: The Bouncer
def rewrite_and_safeguard(inputs: dict) -> str:
    chain = rewrite_prompt | llm | StrOutputParser()
    rewritten = chain.invoke(inputs).strip()
    original = inputs["input"]

    if not rewritten:
        print(f"🛡️ SAFEGUARD: Using original query: '{original}'")
        return original
        
    print(f"✅ REWRITTEN QUERY: '{rewritten}'")
    return rewritten

# Step C: The Final Answer Prompt (Notice we use {standalone_question} here!)
qa_prompt = ChatPromptTemplate.from_template(
    "You are a helpful university assistant. Use the retrieved context to answer the question.\n"
    "If you don't know, say you don't know.\n\n"
    "Context:\n{context}\n\n"
    "Question: {standalone_question}\n"
)

# Step D: The Transparent Chain
# 1. Rewrites the question -> 2. Fetches docs -> 3. Answers the REWRITTEN question
rag_chain = (
    RunnablePassthrough.assign(
        standalone_question=RunnableLambda(rewrite_and_safeguard)
    )
    | RunnablePassthrough.assign(
        context=lambda x: retriever.invoke(x["standalone_question"])
    )
    | qa_prompt
    | llm
    | StrOutputParser()
)

# --- 3. Global Memory & API ---
chat_history = []

class ChatRequest(BaseModel):
    prompt: str

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    global chat_history
    try:
        # The chain now returns a clean string automatically
        answer = rag_chain.invoke({"input": request.prompt, "chat_history": chat_history})
        
        chat_history.append(HumanMessage(content=request.prompt))
        chat_history.append(AIMessage(content=answer))
        
        return {"answer": answer}
    except Exception as e:
        return {"answer": f"System Error: {str(e)}"}

@app.post("/clear")
def clear_memory():
    global chat_history
    chat_history = []
    return {"status": "Memory wiped clean!"}
