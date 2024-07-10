#######################################################
# Agent = Wikipedia + DuckDuckGo
#######################################################
import os
from langchain.utilities import WikipediaAPIWrapper
from langchain.tools import DuckDuckGoSearchRun
from langchain.llms import HuggingFaceEndpoint
from langchain.agents import Tool, initialize_agent
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize API wrappers
wikipedia = WikipediaAPIWrapper()
search = DuckDuckGoSearchRun()

# Initialize HuggingFace LLM
api_key = os.getenv("HUGGINGFACEHUB_API_TOKEN")
if not api_key:
    raise ValueError("HUGGINGFACEHUB_API_TOKEN not found in environment variables")

llm = HuggingFaceEndpoint(
    huggingfacehub_api_token=api_key,
    repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1",
    temperature=0.8,
    max_new_tokens=512,
    streaming=True,
)

# Define tools
tools = [
    Tool(
        name='Wikipedia',
        func=wikipedia.run,
        description="Useful for looking up information about a topic, country, or person on Wikipedia"
    ),
    Tool(
        name='DuckDuckGo Search',
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
    print("You can ask questions, and the AI will try to answer using Wikipedia and DuckDuckGo.")
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

