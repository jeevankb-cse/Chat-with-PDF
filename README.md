# 📄 Chat with PDF (RAG App)

A **Streamlit-based AI application** that allows users to upload PDFs and chat with them using **Retrieval-Augmented Generation (RAG)** powered by LangChain, ChromaDB, HuggingFace embeddings, and Groq LLM.

---

## 🚀 Features

* 📂 Upload PDF files
* 🧠 Ask questions from PDF content
* 🔍 Retrieval-Augmented-Generation (RAG)
* ⚡ Fast embeddings using HuggingFace (`all-MiniLM-L6-v2`)
* 🤖 LLM responses using Groq (LLaMA 3.1)
* 📚 Page number references in answers
* 🌐 Simple Streamlit UI

---

## 🏗️ Tech Stack

* **Frontend:** Streamlit
* **Backend:** Python
* **LLM:** Groq API (LLaMA 3.1 8B Instant)
* **Embeddings:** HuggingFace Sentence Transformers
* **Vector DB:** ChromaDB
* **Framework:** LangChain
* **PDF Processing:** PyPDF

---

## 📁 Project Structure

```
chat_with_pdf/
│── app.py              # Streamlit frontend
│── rag_engine.py       # RAG pipeline (ingestion + QA)
│── requirements.txt    # Dependencies
│── .env                # API keys
│── temp.pdf            # Temporary uploaded file
│── chroma_db/          # Vector database storage
```

---

## ⚙️ Installation

### 1️⃣ Clone the repository

```bash
git clone https://github.com/your-username/chat-with-pdf.git
cd chat-with-pdf
```

---

### 2️⃣ Create virtual environment (IMPORTANT)

Use Python **3.10 recommended**

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

---

### 3️⃣ Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

### 4️⃣ Setup environment variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key_here
```

---

### 5️⃣ Run the app

```bash
streamlit run app.py
```

---

## 🧠 How It Works

1. User uploads a PDF
2. PDF is split into chunks
3. Chunks are embedded using HuggingFace embeddings
4. Stored in Chroma vector database
5. User asks a question
6. Relevant chunks are retrieved
7. Groq LLM generates answer using retrieved context

---

## 📌 Example Usage

* “What is this document about?”
* “Summarize page 2”
* “What are the key points?”
* “Explain section 3 in simple terms”

---

## ⚠️ Requirements Notes

* Use **Python 3.10** for best compatibility
* Avoid Python 3.11+ due to ChromaDB build issues
* Ensure stable versions of LangChain packages

---

## 🔥 Future Improvements

* 📄 Multi-PDF chat support
* ⚡ Streaming responses (ChatGPT-like typing effect)
* 📌 Highlight answers in PDF
* 💾 Persistent chat memory per file


---

## 👨‍💻 Author

Built by **Deeksha Shakyawal**
For learning RAG and real-world LLM apps.

---

