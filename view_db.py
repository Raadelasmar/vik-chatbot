import chromadb

# 1. Connect to your local database folder
client = chromadb.PersistentClient(path="./chroma_db")

# 2. See what collections (tables) exist
print("📚 Available Collections:", client.list_collections())

# 3. Connect to your specific collection
# IMPORTANT: Replace "university_docs" with whatever you named your collection in ingest_database.py!
collection = client.get_collection(name="university_docs") 

# 4. Count how many chunks are inside
print(f"🧩 Total chunks in database: {collection.count()}\n")

# 5. Fetch the first 2 chunks and print them beautifully
data = collection.peek(limit=2)

for i in range(len(data['ids'])):
    print(f"--- 📄 CHUNK {i+1} ---")
    print(f"ID: {data['ids'][i]}")
    print(f"Source PDF: {data['metadatas'][i]}")
    # Print the first 5 numbers of the vector array
    print(f"Vector Math: {data['embeddings'][i][:5]} ... (plus thousands more numbers)") 
    print(f"Text: {data['documents'][i][:150]}...\n")
