import json

from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# -----------------------------
# Load chunks from JSON
# -----------------------------
with open("data/chunks.json", "r", encoding="utf-8") as f:
    chunk_data = json.load(f)

# -----------------------------
# Convert JSON back to Documents
# -----------------------------
documents = []

for chunk in chunk_data:
    documents.append(
        Document(
            page_content=chunk["content"],
            metadata=chunk["metadata"]
        )
    )

print(f"Loaded {len(documents)} chunks")

# -----------------------------
# Create Embedding Model
# -----------------------------
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# -----------------------------
# Create Chroma Vector Database
# -----------------------------
vectorstore = Chroma.from_documents(
    documents=documents,
    embedding=embedding_model,
    persist_directory="chroma_db"
)

print("✅ Vector Database Created Successfully!")