# RAG-ChatBot-With-Gemini

This project is a RAG-based chatbot built using LangChain for document processing, ChromaDB for vector storage, Google Generative AI (Gemini 1.5 Pro) for conversational responses, and Streamlit for the web interface. The chatbot processes uploaded PDFs, extracts text, stores embeddings, and answers user queries intelligently using retrieved document context.

## Features

- **PDF Processing:** Upload a PDF, and the chatbot extracts text and processes it for retrieval.
- **Vector Storage with ChromaDB:** Text chunks are embedded and stored in a ChromaDB vector database for retrieval.
- **Generative AI for Responses:** Uses Google Gemini 1.5 Pro to generate detailed, informative answers.
- **Real-time Interaction:** Users can ask questions related to the PDF, and the app provides accurate responses.
- **Memory Retention:** Maintains conversation history to provide contextual responses.
- **FastAPI Backend:** API endpoints for PDF upload, querying, and clearing data.

## Technologies Used

- **LangChain:** Framework for document processing and retrieval.
- **ChromaDB:** High-performance vector database for storing embeddings.
- **Google Generative AI (Gemini 1.5 Pro):** LLM for generating intelligent responses.
- **Streamlit:** Web-based framework for creating interactive UIs.
- **FastAPI:** Backend framework for API endpoints.
- **Python:** For all backend functionality.

## Installation

To run this project locally, follow these steps:

1. Clone the repository:

   ```sh
   git clone https://github.com/AbhiMAtGitHub/ChatBot_Project.git
   cd RAG-ChatBot-With-Gemini
   ```

2. Install the dependencies:

   ```sh
   pip install -r requirements.txt
   ```

3. Set up your API keys (Create a `.env` file and add your Google AI API key):

   ```sh
   GOOGLE_API_KEY=your-google-generative-ai-key
   ```

4. Start FastAPI Backend:

   ```sh
   uvicorn app.main:app --host 0.0.0.0 --port 7077 --reload --log-level debug
   ```

5. Run Streamlit Frontend:

   ```sh
   cd frontend
   streamlit run chatbot_ui.py
   ```

## Project Structure

```
RAG-ChatBot-With-Gemini
│── app
│   ├── services          # Core services (vector storage, chatbot logic)
│   ├── config            # Configuration settings
│   ├── routes            # FastAPI endpoints
│   ├── main.py           # FastAPI main entry point
│
│── frontend
│   ├── chatbot_ui.py     # Streamlit UI
│
│── requirements.txt      # Project dependencies
│── README.md            # Project documentation
```

## API Endpoints

| Method  | Endpoint  | Description |
|---------|----------|-------------|
| **POST**  | `/upload/` | Uploads a PDF file, extracts text, and stores embeddings in ChromaDB. |
| **POST**  | `/ask/` | Processes user queries and retrieves responses using RAG pipeline. |
| **DELETE** | `/clear/` | Clears stored chat history and vector database. |

## How It Works

1. **PDF Upload:** Users upload a PDF file, and text is extracted and processed into chunks.
2. **Embedding & Storage:** Extracted text chunks are embedded using Google AI embeddings and stored in ChromaDB.
3. **Query Processing:** When a user asks a question, relevant document chunks are retrieved using MMR technique.
4. **AI Response Generation:** The Gemini 1.5 Pro model generates a contextual response based on retrieved information and past chat history.
5. **Real-Time Chat:** The chatbot responds interactively via the Streamlit UI.
