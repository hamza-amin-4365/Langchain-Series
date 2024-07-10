#######################################################
# Agent = Tavily + DuckDuckGo
#######################################################

import os
from langchain_community.retrievers import TavilySearchAPIRetriever
from langchain.tools import DuckDuckGoSearchRun
from langchain.agents import Tool, initialize_agent
from langchain.llms import HuggingFaceEndpoint
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize TavilySearchAPIRetriever
tavily_retriever = TavilySearchAPIRetriever(
    api_key=os.getenv("TAVILY_API_KEY"),
    k=3,
)

# Initialize DuckDuckGo search
search = DuckDuckGoSearchRun()

# Initialize HuggingFace LLM
api_key = os.getenv("huggingfacehub_api_token")
if not api_key:
    raise ValueError("huggingfacehub_api_token not found in environment variables")

llm = HuggingFaceEndpoint(
    huggingfacehub_api_token=api_key,
    repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1",
    temperature=0.8,
    max_new_tokens=512,
    streaming=True,
)

# Define Tavily retriever function
def TavilySearch(query):
    try:
        results = tavily_retriever.invoke(query)
        if isinstance(results, list) and results:
            content_list = [doc.page_content for doc in results]
            return ' '.join(content_list)
        return "No relevant information found."
    except Exception as e:
        return f"An error occurred during Tavily AI search: {str(e)}"

# Define tools
tools = [
    Tool(
        name='TavilySearch',
        func=TavilySearch,
        description="Useful for searching the internet using Tavily AI for high-quality information"
    ),
    Tool(
        name='DuckDuckGoSearch',
        func=search.run,
        description="Useful for searching the internet for information not found in other tools"
    )
]

# Initialize agent
agent = initialize_agent(
    agent="zero-shot-react-description",
    tools=tools,
    llm=llm,
    verbose=True,
    max_iterations=3,
)

def main():
    print("Welcome to the AI Assistant!")
    print("You can ask questions, and the AI will try to answer using Tavily AI and DuckDuckGo.")
    print("Type 'quit' to exit the program.")

    while True:
        question = input("\nEnter your question: ").strip()
        if question.lower() == 'quit':
            print("Thank you for using the AI Assistant. Goodbye!")
            break

        try:
            answer = agent.run(question)
            print(f"\nAnswer: {answer}")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()