import os
from dotenv import load_dotenv

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEndpointEmbeddings

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# -------------------------
# Load Environment Variables
# -------------------------

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")

# -------------------------
# Embedding Model
# -------------------------

embedding = HuggingFaceEndpointEmbeddings(
    model="sentence-transformers/all-MiniLM-L6-v2",
    huggingfacehub_api_token=os.getenv("HF_TOKEN")
)

# -------------------------
# Load Chroma DB
# -------------------------

vectorstore = Chroma(
    persist_directory="chroma_db",
    embedding_function=embedding
)

retriever = vectorstore.as_retriever(
    search_kwargs={"k":3}
)

# -------------------------
# Load LLM
# -------------------------

llm = ChatGroq(
    groq_api_key=groq_api_key,
    model_name="llama-3.3-70b-versatile"
)

# -------------------------
# Prompt
# -------------------------

prompt = ChatPromptTemplate.from_template(
"""
You are a helpful AI assistant.

Answer the user's question ONLY using the provided context.

If the answer is not available in the context, reply:

"I couldn't find this information in the Bank of America credit card documents."

Context:
{context}

Question:
{question}

Answer:
"""
)

# -------------------------
# Convert retrieved docs to text
# -------------------------

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# -------------------------
# Build LCEL RAG Chain
# -------------------------

chain = (
    {
        "context": retriever | format_docs,
        "question": RunnablePassthrough()
    }
    | prompt
    | llm
    | StrOutputParser()
)

# -------------------------
# Ask Function
# -------------------------

def ask(question):

    # Generate Answer
    answer = chain.invoke(question)

    # Retrieve documents
    docs = retriever.invoke(question)

    sources = []

    for doc in docs:
        sources.append({
            "card_name": doc.metadata.get("card_name", "Unknown"),
            "source": doc.metadata.get("source", "Unknown"),
            "content": doc.page_content
        })

    return {
        "answer": answer,
        "sources": sources
    }