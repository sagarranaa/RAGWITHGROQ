import streamlit as st
import tempfile
import os
from dotenv import load_dotenv

load_dotenv()

# LangChain
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# Groq
from langchain_groq import ChatGroq


# ---------------- UI ----------------
st.set_page_config(page_title="RAG Chat App")
st.title("Chat with your PDF (Memory Enabled)")

uploaded_file = st.file_uploader("Upload PDF", type="pdf")


# ---------------- Session State ----------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "vector_db" not in st.session_state:
    st.session_state.vector_db = None


# ---------------- Vector DB ----------------
@st.cache_resource
def create_vectorstore(file_path):
    loader = PyPDFLoader(file_path)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )
    chunks = splitter.split_documents(docs)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    return FAISS.from_documents(chunks, embeddings)


# ---------------- LLM ----------------
@st.cache_resource
def load_llm():
    return ChatGroq(
        model=os.getenv("GROQ_MODEL"),  # from .env
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0
    )


# ---------------- Prompt ----------------
prompt = PromptTemplate.from_template("""
You are an AI assistant.

Use the chat history and context to answer.

Chat History:
{history}

Context:
{context}

Question:
{question}

Answer:
""")


# ---------------- Main ----------------
if uploaded_file is not None:

    if uploaded_file.type != "application/pdf":
        st.error("Upload a valid PDF")
        st.stop()

    # Process only once
    if st.session_state.vector_db is None:
        st.info("Processing PDF...")

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded_file.read())
            file_path = tmp.name

        try:
            st.session_state.vector_db = create_vectorstore(file_path)
            st.success("PDF Ready ✅")
        except Exception as e:
            st.error(f"Error: {e}")
            st.stop()

    db = st.session_state.vector_db
    retriever = db.as_retriever(search_kwargs={"k": 4})
    llm = load_llm()

    # Display chat history
    for chat in st.session_state.chat_history:
        with st.chat_message(chat["role"]):
            st.write(chat["content"])

    # User input
    user_input = st.chat_input("Ask something about the PDF")

    if user_input:

        # Save user message
        st.session_state.chat_history.append({
            "role": "user",
            "content": user_input
        })

        with st.chat_message("user"):
            st.write(user_input)

        # Prepare history text
        history_text = "\n".join(
            [f"{c['role']}: {c['content']}" for c in st.session_state.chat_history]
        )

        def format_docs(docs):
            return "\n\n".join(d.page_content for d in docs)

        rag_chain = (
            {
                "context": retriever | format_docs,
                "question": RunnablePassthrough(),
                "history": lambda _: history_text
            }
            | prompt
            | llm
            | StrOutputParser()
        )

        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = rag_chain.invoke(user_input)
                    st.write(response)

                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": response
                    })

                except Exception as e:
                    st.error(f"Error: {e}")