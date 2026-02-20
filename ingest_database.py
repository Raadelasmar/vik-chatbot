import os
import shutil
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from uuid import uuid4

load_dotenv()

DATA_PATH = "data"
CHROMA_PATH = "chroma_db"

# 1. Clear Old Data
if os.path.exists(CHROMA_PATH):
    try:
        shutil.rmtree(CHROMA_PATH)
        print(f"🗑️ Old database '{CHROMA_PATH}' cleared.")
    except Exception as e:
        print(f"⚠️ Warning: Could not delete old database: {e}")

if not os.path.exists(DATA_PATH):
    os.makedirs(DATA_PATH)
    print(f"⚠️ Created '{DATA_PATH}' directory. Please put your PDFs inside and run again.")
    exit()

# 2. Setup Embeddings
try:
    embeddings_model = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
except Exception as e:
    print(f"❌ Error initializing embeddings model: {e}")
    exit()

# 3. Load PDFs
try:
    loader = PyPDFDirectoryLoader(DATA_PATH)
    raw_documents = loader.load()
    if not raw_documents:
        print(f"⚠️ No PDFs found.")
        exit()
except Exception as e:
    print(f"❌ Error loading PDFs: {e}")
    exit()

# 4. The UPGRADED Smart Splitter
text_splitter = RecursiveCharacterTextSplitter(
    separators=[
        "\nSubject code",
        "\nCourse Syllabus",
        '\n"BMEVI',            # FIXED: Catches the PDF quotation marks!
        "\nBMEVI",
        '\n"BMEGT',            # FIXED: Catches the PDF quotation marks!
        "\nBMEGT",
        "\n\n",
        "\n",
        " "
    ],
    chunk_size=1500,           # INCREASED: Swallows whole course blocks easily
    chunk_overlap=300,         # INCREASED: Massive safety net for tabular data
    length_function=len,
    is_separator_regex=False,
)

chunks = text_splitter.split_documents(raw_documents)
print(f"✅ Split {len(raw_documents)} pages into {len(chunks)} ultra-smart chunks.")

# 5. Save to Chroma
try:
    vector_store = Chroma(
        collection_name="vik_collection",
        embedding_function=embeddings_model,
        persist_directory=CHROMA_PATH,
    )
    uuids = [str(uuid4()) for _ in range(len(chunks))]
    vector_store.add_documents(documents=chunks, ids=uuids)
    print(f"🚀 Ingestion complete! Database saved to '{CHROMA_PATH}'.")
except Exception as e:
    print(f"❌ Error saving to Chroma database: {e}")
