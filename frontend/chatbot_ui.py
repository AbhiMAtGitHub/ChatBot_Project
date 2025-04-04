import streamlit as st
import requests

API_URL = "http://localhost:7077"

st.title("🤖 RAG Chatbot with Gemini")

# File Upload Section
st.sidebar.header("📂 Upload PDFs")
uploaded_files = st.sidebar.file_uploader("Choose PDF files", type="pdf", accept_multiple_files=True)

if uploaded_files and st.sidebar.button("📤 Upload Files"):
    with st.sidebar:
        st.write("Uploading...")
        files = [("files", (file.name, file.getvalue(), "application/pdf")) for file in uploaded_files]
        res = requests.post(f"{API_URL}/upload/", files=files)
        
        if res.status_code == 200:
            response = res.json()
            for file_status in response["details"]:
                if "Processed successfully" in file_status["status"]:
                    st.success(f"{file_status['filename']} ✅")
                else:
                    st.error(f"{file_status['filename']} ❌ {file_status['status']}")
        else:
            st.error("Failed to upload PDFs.")

# Chat Section
st.subheader("💬 Chat with your AI")
user_input = st.text_input("Type your question:", "")

if st.button("Ask"):
    if user_input:
        res = requests.post(f"{API_URL}/ask/", json={"query": user_input})
        if res.status_code == 200:
            response = res.json()["response"]
            st.write("🤖:", response)
        else:
            st.error("Error fetching response.")

# Clear Button
if st.sidebar.button("🗑️ Clear Chat & Memory"):
    res = requests.delete(f"{API_URL}/clear/")
    if res.status_code == 200:
        st.success("Chat history and memory cache has been cleared!")
    else:
        st.error("Failed to clear data.")
