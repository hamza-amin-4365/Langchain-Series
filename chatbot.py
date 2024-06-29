import os
from dotenv import load_dotenv
import streamlit as st
from langchain.llms import HuggingFaceEndpoint
import wikipedia

# Load API key from .env file
load_dotenv()
api_key = os.getenv("HUGGINGFACEHUB_API_TOKEN")

# Initialize Hugging Face API client
client = HuggingFaceEndpoint(repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1", token=api_key)

def search_wikipedia(query, sentences=2):
    try:
        return wikipedia.summary(query, sentences=sentences)
    except:
        return "No relevant information found on Wikipedia."

def generate_response(prompt, wiki_info):
    combined_input = f"Based on the following Wikipedia information: '{wiki_info}'\n\nUser question: {prompt}\n\nProvide a comprehensive answer:"
    response = client.invoke(combined_input, parameters={"temperature": 0.8, "max_length": 300})
    return response

st.title("AI Tutor with Wikipedia Integration")
st.write("Hi! I'm here to help you with your homework. I'll search Wikipedia and combine that with my knowledge to provide accurate information. Feel free to ask anything, but remember not to copy and paste!")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What would you like to know?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Searching Wikipedia and generating response..."):
            wiki_info = search_wikipedia(prompt)
            response = generate_response(prompt, wiki_info)
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})