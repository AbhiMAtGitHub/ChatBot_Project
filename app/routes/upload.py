from fastapi import APIRouter, UploadFile, File, HTTPException
import os
from app.services.vectorstore import vectorstore, embeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

router = APIRouter()

@router.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    file_path = f"temp_{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())

    try:
        loader = PyPDFLoader(file_path)
        data = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        docs = text_splitter.split_documents(data)

        #Ensure vectorstore is properly initialized before modifying it
        if vectorstore is None:
            raise HTTPException(status_code=500, detail="Vectorstore is not initialized!")

        vectorstore.add_documents(docs)
        return {"message": f"File '{file.filename}' uploaded and processed successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        os.remove(file_path)  #Cleanup temp file after processing
