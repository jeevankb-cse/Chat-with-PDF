import os
import gc
from functools import lru_cache
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from chromadb.config import Settings

os.environ["ANONYMIZED_TELEMETRY"] = "False"
os.environ["CHROMA_TELEMETRY_ENABLED"] = "False"

# Belt-and-suspenders: neuter telemetry at the source so version
# mismatches between chromadb <-> posthog can never surface as
# noisy log errors, regardless of the Settings() flag above.
import chromadb.telemetry.product.posthog as chroma_telemetry
chroma_telemetry.Posthog.capture = lambda *args, **kwargs: None



load_dotenv()

DB_DIR = "/tmp/chroma_db"
COLLECTION_NAME = "pdf_collection"

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    groq_api_key=os.getenv("GROQ_API_KEY")
)

# ----------------------------
# Cache ONLY the embedding model (expensive to load).
# Do NOT cache the Chroma db object — it must always
# reflect whatever collection currently exists on disk.
# ----------------------------
@lru_cache(maxsize=1)
def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

def ingest_pdf(pdf_path):
    gc.collect()

    loader = PyPDFLoader(pdf_path)
    pages = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=200
    )
    docs = splitter.split_documents(pages)

    embeddings = get_embeddings()

    # Clean slate: wipe any existing collection first
    try:
        existing = Chroma(
            persist_directory=DB_DIR,
            embedding_function=embeddings,
            collection_name=COLLECTION_NAME
        )
        existing.delete_collection()
    except Exception:
        pass

    db = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        persist_directory=DB_DIR,
        collection_name=COLLECTION_NAME
    )
    

    os.remove(pdf_path)
    return len(docs)

# ----------------------------
# Build a FRESH Chroma handle every call.
# This is cheap — it just opens the existing persist_directory,
# it does NOT reload/re-embed anything.
# ----------------------------
def load_db():
    embeddings = get_embeddings()
    return Chroma(
        persist_directory=DB_DIR,
        embedding_function=embeddings,
        collection_name=COLLECTION_NAME,
        client_settings=Settings(anonymized_telemetry=False)
    )

def query(question, history):
    db = load_db()
    retriever = db.as_retriever(search_kwargs={"k": 4})
    docs = retriever.invoke(question)

    context = "\n\n".join([d.page_content for d in docs])

    recent_history = history[-6:]
    history_text = ""
    for h in recent_history:
        history_text += f"User: {h['user']}\nAssistant: {h['bot']}\n"

    prompt = f"""
You are an AI assistant answering questions from a PDF.

Context:
{context}

Conversation history:
{history_text}

Rules:
- Answer ONLY using the given context
- If answer is not in context, say: "I don't have that information."

Question: {question}

Answer:
"""

    response = llm.invoke(prompt)
    answer = response.content if hasattr(response, "content") else str(response)

    pages = sorted(set([d.metadata.get("page", 0) + 1 for d in docs]))
    return answer, pages