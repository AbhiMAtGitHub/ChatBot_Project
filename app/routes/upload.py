from fastapi import APIRouter, UploadFile, File, HTTPException
import os
from app.services.vectorstore import vectorstore
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

router = APIRouter()

@router.post("/upload/")
async def upload_files(files: list[UploadFile] = File(...)):
    if not files:
        raise HTTPException(status_code=400, detail="No files uploaded!")

    responses = []
    
    for file in files:
        file_path = f"temp_{file.filename}"
        with open(file_path, "wb") as f:
            f.write(await file.read())

        try:
            loader = PyPDFLoader(file_path)
            data = loader.load()
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
            docs = text_splitter.split_documents(data)

            if vectorstore is None:
                raise HTTPException(status_code=500, detail="Vectorstore is not initialized!")

            vectorstore.add_documents(docs)
            responses.append({"filename": file.filename, "status": "Processed successfully"})
        except Exception as e:
            responses.append({"filename": file.filename, "status": f"Failed - {str(e)}"})
        finally:
            os.remove(file_path)  # Cleanup temp file

    return {"message": "Files processed", "details": responses}
