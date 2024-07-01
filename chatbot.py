import os
from dotenv import load_dotenv
import streamlit as st
from huggingface_hub import InferenceClient
from duckduckgo_search import DDGS
from langchain_community.retrievers import WikipediaRetriever
from typing import Any

retriver = WikipediaRetriever()

load_dotenv()
api_key = os.getenv("HUGGINGFACEHUB_API_TOKEN")

# Custom StreamHandler for Streamlit
class StreamlitCallbackHandler:
    def __init__(self, container):
        self.container = container
        self.text = ""

    def __call__(self, token: str, **kwargs: Any) -> None:
        self.text += token
        self.container.markdown(self.text)

client = InferenceClient(model="mistralai/Mixtral-8x7B-Instruct-v0.1", token=api_key)

def search_wikipedia(query):
    try:
        return retriver.invoke(query)
    except:
        return "No relevant information found on Wikipedia."

def search_duckduckgo(query, num_results=3):
    with DDGS() as ddgs:
        results = [r for r in ddgs.text(query, max_results=num_results)]
    return "\n".join([f"Title: {r['title']}\nSnippet: {r['body']}" for r in results])

def generate_response(prompt, wiki_info, ddg_info, stream_container):
    combined_input = f"""Based on the following information:

Wikipedia: '{wiki_info}'

DuckDuckGo Search Results:
{ddg_info}

User question: {prompt}

Provide a comprehensive and accurate answer, combining the above information with your own knowledge:"""
    
    stream_handler = StreamlitCallbackHandler(stream_container)
    
    for token in client.text_generation(combined_input, max_new_tokens=300, temperature=0.7, stream=True):
        stream_handler(token)
    
    return stream_handler.text

st.title("AI Tutor with Wikipedia and DuckDuckGo Integration")
st.write("Hi! I'm here to help you with your homework. I'll search Wikipedia and the internet, then combine that with my knowledge to provide accurate information. Feel free to ask anything, but remember not to copy and paste!")

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
        with st.spinner("Searching Wikipedia and DuckDuckGo..."):
            wiki_info = search_wikipedia(prompt)
            ddg_info = search_duckduckgo(prompt)
        
        stream_container = st.empty()
        response = generate_response(prompt, wiki_info, ddg_info, stream_container)
        
    st.session_state.messages.append({"role": "assistant", "content": response})