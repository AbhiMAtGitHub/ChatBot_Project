from fastapi import FastAPI
from app.routes import ask, upload, clear

app = FastAPI(title="Modular RAG Chatbot API", version="1.0")

# Register Routes
app.include_router(ask.router)
app.include_router(upload.router)
app.include_router(clear.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7077)
