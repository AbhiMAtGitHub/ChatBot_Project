import streamlit as st
import requests

API_URL = "http://localhost:7077"

st.title("🤖 RAG Chatbot with Gemini")

# File Upload Section
st.sidebar.header("📂 Upload a PDF")
uploaded_file = st.sidebar.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file and st.sidebar.button("📤 Upload File"):  # Upload only when the button is clicked
    with st.sidebar:
        st.write("Uploading...")
        files = {"file": uploaded_file.getvalue()}
        res = requests.post(f"{API_URL}/upload/", files=files)
        if res.status_code == 200:
            st.success(res.json()["message"])
        else:
            st.error("Failed to upload PDF.")

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
