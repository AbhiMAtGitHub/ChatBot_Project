from fastapi import APIRouter, HTTPException
from app.services.chatbot import memory  #Import memory properly

router = APIRouter()

@router.delete("/clear/")
async def clear_chat():
    """Clears only the chat memory (not the vectorstore)."""
    try:
        if memory:
            memory.clear()
        return {"message": "Chat memory cleared successfully!"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
