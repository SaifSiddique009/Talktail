import streamlit as st
import requests
from dotenv import load_dotenv
import os
load_dotenv('../.env')

# Detect local vs cloud 
API_URL = os.environ.get('BACKEND_URL', 'http://localhost:8001/api/chat')  

st.title("Product Chatbot")

# Pre-written queries
pre_queries = [
    "What’s the price of kiwi?",
    "Do you have any electronics?",
    "Show me products with ratings above 4.",
    "Tell me the reviews for volleyball."
]

# Session state for key
if "groq_api_key" not in st.session_state:
    st.session_state.groq_api_key = os.getenv('GROQ_API_KEY')  # Auto-load from env

# Key input (always show, but pre-filled if env)
if not st.session_state.groq_api_key:
    groq_key = st.text_input("Enter your Groq API Key (required):", type="password")
    if groq_key:
        st.session_state.groq_api_key = groq_key
else:
    groq_key = st.text_input("Enter your Groq API Key:", value=st.session_state.groq_api_key)
    if groq_key:
        st.session_state.groq_api_key = groq_key

# Query selectbox
selected_query = st.selectbox("Choose a sample query:", [""] + pre_queries)
message = st.text_input("Or ask your own:", value=selected_query)

if st.button("Send") and message and st.session_state.groq_api_key:
    try:
        payload = {"message": message, "groq_api_key": st.session_state.groq_api_key}
        response = requests.post(API_URL, json=payload)
        response.raise_for_status()
        st.write("Response:", response.json()["response"])
    except Exception as e:
        st.error(f"Error: {e}")