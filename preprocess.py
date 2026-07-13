import json

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Load scraped data
with open("data/raw_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

documents = []

# Convert JSON to LangChain Documents
for item in data:

    text = f"""
Card Name: {item['card_name']}

Category: {item['category']}

Description:
{item['description']}

Features:
{" ".join(item['features'])}

Benefits:
{item['benefits']}

Rates & Fees:
{" ".join(item['rates_fees'])}
"""

    documents.append(
        Document(
            page_content=text,
            metadata={
                "source": item["source"],
                "card_name": item["card_name"]
            }
        )
    )

# Split into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

chunks = text_splitter.split_documents(documents)

# Convert chunks to JSON format
chunk_data = []

for i, chunk in enumerate(chunks):
    chunk_data.append({
        "chunk_id": i + 1,
        "content": chunk.page_content,
        "metadata": chunk.metadata
    })

# Save chunks to JSON
with open("data/chunks.json", "w", encoding="utf-8") as f:
    json.dump(chunk_data, f, indent=4, ensure_ascii=False)

print(f"Total Documents : {len(documents)}")
print(f"Total Chunks : {len(chunks)}")
print("Chunks saved to data/chunks.json")