from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.chatbot import get_response

router = APIRouter()

class QueryRequest(BaseModel):
    query: str

@router.post("/ask/")
async def ask_question(request: QueryRequest):
    try:
        response = get_response(request.query)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
