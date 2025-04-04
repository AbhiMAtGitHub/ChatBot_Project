from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.memory import ConversationBufferMemory
from app.services.vectorstore import retriever
from app.config.settings import GOOGLE_API_KEY

# Initialize LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro", temperature=0.8, max_tokens=1024, google_api_key=GOOGLE_API_KEY, streaming=True
)

# Memory for chat history
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Define Prompt
system_prompt = (
    "You are a highly knowledgeable AI assistant. Use the retrieved context to answer the user's questions "
    "in a **detailed, structured, and informative manner**.\n\n"
    "💡 **Guidelines for Your Response:**\n"
    "- Provide **in-depth explanations** with relevant **examples**.\n"
    "- **Break down complex topics** into **simpler steps**.\n"
    "- Include **technical details** where necessary.\n"
    "- If possible, **give multiple perspectives** on the answer.\n"
    "- If you **don’t know** the answer, say so.\n\n"
    "**Previous conversation history:**\n{chat_history}\n\n"
    "**Context:**\n{context}"
)

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}"),
])

# Create RAG Pipeline
question_answer_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)

def get_response(query):
    """Processes user query and returns chatbot response."""
    chat_history = memory.load_memory_variables({}).get("chat_history", [])
    response = rag_chain.invoke({"input": query, "chat_history": chat_history})
    memory.save_context({"input": query}, {"output": response.get("answer", "No response generated.")})
    return response.get("answer", "No response generated.")

def clear_memory():
    """Clears conversation history."""
    memory.clear()
