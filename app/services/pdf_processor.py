from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from app.services.vectorstore import vectorstore, embeddings
from app.config.settings import CHUNK_SIZE, CHUNK_OVERLAP

def process_pdf(file_path):
    """Loads, splits, and stores the PDF content in ChromaDB."""
    loader = PyPDFLoader(file_path)
    data = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    docs = text_splitter.split_documents(data)

    if vectorstore is None:
        raise ValueError("Vectorstore is not initialized!")

    #Add documents to existing vectorstore instead of overwriting
    vectorstore.add_documents(docs)

    return "PDF processed and stored in vector database."
