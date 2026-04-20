# 🚀 RAG Chat with PDF (Groq Powered)

An AI-powered application that allows users to upload PDFs and interact with them using natural language. Built using Retrieval-Augmented Generation (RAG) with fast inference powered by Groq.

---
<img width="1848" height="1053" alt="groq2" src="https://github.com/user-attachments/assets/837a3bf2-4d39-4a31-ad53-9d9c25fa470a" />
<img width="1848" height="1053" alt="groq1" src="https://github.com/user-attachments/assets/9f3e50f3-debb-4b18-8b03-6ad581da84b7" />



## 📌 Features

* 📄 Upload and process PDF documents
* 💬 Chat with your PDF like ChatGPT
* 🧠 Context-aware answers using conversation memory
* ⚡ Fast responses using Groq LLM
* 🔍 Semantic search with FAISS vector database
* 🛡️ Error handling for invalid/corrupted files

---

## 🧠 How It Works

This project uses a **RAG (Retrieval-Augmented Generation)** pipeline:

1. PDF is uploaded and parsed
2. Text is split into smaller chunks
3. Chunks are converted into embeddings
4. Stored in FAISS vector database
5. User asks a question
6. Relevant chunks are retrieved
7. Sent to LLM (Groq) for answer generation

---

## 🏗️ Tech Stack

* Frontend: Streamlit
* Backend: LangChain
* LLM: Groq (LLaMA 3.1)
* Embeddings: Sentence Transformers
* Vector DB: FAISS

---

## 📂 Project Structure

```
rag-groq-app/
│── app.py
│── requirements.txt
│── .env
│── README.md
```

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/your-username/rag-groq-app.git
cd rag-groq-app
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Add environment variables

Create a `.env` file:

```
GROQ_API_KEY=your_api_key_here
GROQ_MODEL=llama-3.1-8b-instant
```

---

### 4. Run the application

```bash
streamlit run app.py
```

---

## 🎯 Usage

1. Upload a PDF file
2. Wait for processing
3. Ask questions about the document
4. Get context-aware answers instantly

---

## 🚀 Use Cases

* 📚 Study assistant for textbooks
* 🏢 Company document search
* ⚖️ Legal document analysis
* 💼 Financial report insights
* 🏥 Medical document Q&A

---

## ⚠️ Limitations

* Depends on quality of PDF text
* No reranking (basic retrieval)
* May miss context in some cases

---

## 🔮 Future Improvements

* Multi-PDF support
* Source citations with page numbers
* Better retrieval (reranking)
* Chat streaming responses
* Deployment (AWS / Streamlit Cloud)

---

## 👨‍💻 Author

Sagar Rana

---

## ⭐ If you like this project

Give it a star ⭐ on GitHub!
