import streamlit as st
from rag_api import ask

# -------------------------
# Page Configuration
# -------------------------

st.set_page_config(
    page_title="Bank of America Credit Card RAG",
    page_icon="💳",
    layout="wide"
)

st.title("💳 Bank of America Credit Card RAG")
st.write("Ask questions about Bank of America Credit Cards using Retrieval-Augmented Generation (RAG).")

# -------------------------
# User Input
# -------------------------

question = st.text_input(
    "Enter your question:",
    placeholder="Example: What travel rewards cards are available?"
)

# -------------------------
# Search Button
# -------------------------

if st.button("Get Answer"):

    if question.strip() == "":
        st.warning("Please enter a question.")
    else:

        with st.spinner("Searching documents and generating answer..."):

            result = ask(question)

        # -------------------------
        # Answer
        # -------------------------

        st.subheader("Answer")

        st.success(result["answer"])

        # -------------------------
        # Sources
        # -------------------------

        st.subheader("Retrieved Sources")

        if len(result["sources"]) == 0:
            st.info("No source documents found.")

        for i, source in enumerate(result["sources"], start=1):

            with st.expander(f"Source {i} - {source['card_name']}"):

                st.markdown(f"**Card Name:** {source['card_name']}")

                st.markdown(f"**Source URL:** {source['source']}")

                st.markdown("**Retrieved Content:**")

                st.write(source["content"])