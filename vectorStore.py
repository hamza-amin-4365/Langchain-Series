from langchain.llms import HuggingFaceEndpoint
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.vectorstores import VectorStoreRetriever
from langchain.chains import RetrievalQA
import os
from dotenv import load_dotenv
import langchain_community.document_loaders as doc_loaders

loader = doc_loaders.TextLoader("/path to your txtual data")  
documents = loader.load()
text_splitter = RecursiveCharacterTextSplitter(
chunk_size=500,
chunk_overlap=0,
length_function=len,
)
docs = text_splitter.split_documents (documents)
load_dotenv()
embeddings = HuggingFaceInferenceAPIEmbeddings(
    api_key=os.getenv("embedding_api_key"),
    model_name="sentence-transformers/all-MiniLM-l6-v2",
)
library = FAISS.from_documents(docs, embeddings)
retriever = library.as_retriever()
api_key = os.getenv("huggingfacehub_api_token")
llm = HuggingFaceEndpoint(
    huggingfacehub_api_token=api_key,
    repo_id="mistralai/Mistral-7B-Instruct-v0.3",
    temperature=0.7,
    max_new_tokens=1024,
)
library.save_local("fiass_index_metallica")

metallica_saved = FAISS.load_local("fiass_index_metallica", embeddings, allow_dangerous_deserialization=True)
qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=metallica_saved.as_retriever())

question = "Question about your text which you made a vector store from."
res = qa.invoke(question)
print(res)
