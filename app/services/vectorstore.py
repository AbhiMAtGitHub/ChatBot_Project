from langchain_chroma import Chroma
from app.config.settings import GOOGLE_API_KEY, PERSIST_DIRECTORY
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# Load Google AI Embeddings
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=GOOGLE_API_KEY)

# Initialize ChromaDB vectorstore
vectorstore = Chroma(persist_directory=PERSIST_DIRECTORY, embedding_function=embeddings)
retriever = vectorstore.as_retriever(search_type="mmr", search_kwargs={"k": 20, "fetch_k": 50})

def clear_vectorstore():
    """Deletes all documents from ChromaDB."""
    vectorstore.delete_collection()
