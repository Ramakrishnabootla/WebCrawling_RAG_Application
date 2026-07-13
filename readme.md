# Bank of America Credit Card RAG

## Instructions to Run the Project

### Step 1: Install the Required Libraries

```bash
pip install -r requirements.txt
```

---

### Step 2: Run the Crawler

This script scrapes the Bank of America Credit Cards website and saves the extracted data in `raw_data.json`.

```bash
python crawler.py
```

---

### Step 3: Preprocess the Data

This script cleans the scraped data, converts it into LangChain documents, splits the text into chunks, and saves the chunks in `chunks.json`.

```bash
python preprocess.py
```

---

### Step 4: Build the Vector Store

This script generates embeddings for all chunks and stores them in the Chroma Vector Database.

```bash
python index.py
```

---

### Step 5: Run the RAG Application

Start the Streamlit application.

```bash
streamlit run app.py
```

Open the URL displayed in the terminal (usually `http://localhost:8501`) in your browser.

---

# Example Queries

You can try asking questions like:

* What travel rewards cards are available
* Which cards offer cash back
* What are the benefits of the Travel Rewards Credit Card
* Which cards have no annual fee
* Tell me about the rewards programs.
* Which credit cards have lower interest rates

---

# Project Workflow

```
Bank of America Website
          │
          ▼
      crawler.py
          │
          ▼
    raw_data.json
          │
          ▼
    preprocess.py
          │
          ▼
     chunks.json
          │
          ▼
       index.py
          │
          ▼
   Chroma Vector Database
          │
          ▼
      rag_api.py
          │
          ▼
       app.py
```
