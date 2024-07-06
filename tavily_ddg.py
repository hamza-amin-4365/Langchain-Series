import os
from langchain_community.retrievers import TavilySearchAPIRetriever
from langchain.tools import DuckDuckGoSearchRun
from langchain.agents import Tool, initialize_agent, AgentType
from langchain.llms import HuggingFaceEndpoint
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain_core.prompts import ChatPromptTemplate


load_dotenv()


tavily_retriever = TavilySearchAPIRetriever(
    api_key=os.getenv("TAVILY_API_KEY"),
    k=3,
)

search = DuckDuckGoSearchRun()

api_key = os.getenv("huggingfacehub_api_token")
if not api_key:
    raise ValueError("huggingfacehub_api_token not found in environment variables")


llm = HuggingFaceEndpoint(
    huggingfacehub_api_token=api_key,
    repo_id="mistralai/Mistral-7B-Instruct-v0.3",
    temperature=0.7,
    max_new_tokens=1024,
)



tools = [
    Tool(
        name='TavilySearch',
        func=tavily_retriever.invoke,
        description="Useful for searching the internet using Tavily AI for high-quality information"
    ),
    Tool(
        name='DuckDuckGoSearch',
        func=search.run,
        description="Useful for searching the internet for information not found in other tools"
    ),
]

fixed_prompt = PromptTemplate(
input_variables=['agent_scratchpad', 'input'],
template = """Answer the following questions as best you can. You have access to the following tools:

TavilySearch(input: 'str', config: 'Optional[RunnableConfig]' = None, **kwargs: 'Any') -> 'List[Document]' - Useful for searching the internet using Tavily AI for high-quality information
DuckDuckGoSearch(tool_input: 'Union[str, Dict[str, Any]]', verbose: 'Optional[bool]' = None, start_color: 'Optional[str]' = 'green', color: 'Optional[str]' = 'green', callbacks: 'Callbacks' = None, *, tags: 'Optional[List[str]]' = None, metadata: 'Optional[Dict[str, Any]]' = None, run_name: 'Optional[str]' = None, run_id: 'Optional[uuid.UUID]' = None, config: 'Optional[RunnableConfig]' = None, **kwargs: 'Any') -> 'Any' - Useful for searching the internet for information not found in other tools

Use the following format:

Question: {input}
Thought: {agent_scratchpad}
Action: the action to take, should be one of [TavilySearch, DuckDuckGoSearch]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
# Final Answer: the final answer to the original input question

Example format of your response:
    Simple Harmonic Motion (SHM) is a type of periodic motion where an object oscillates back and forth around an equilibrium position,
    driven by a restoring force proportional to its displacement. The displacement x(t) can be described by the equation:

    x(t) = Acos(ωt + ϕ)

    where:
    - A is the amplitude,
    - ω is the angular frequency,
    - ϕ is the phase angle.

    The period T and frequency f are related by T = 1/f and ω = 2πf. The total mechanical energy E in SHM is conserved and can be expressed as E = 1/2 k A^2, where k is the spring constant in a mass-spring system.

    Common examples of SHM include a mass on a spring, described by Hooke's Law F = -kx, and a simple pendulum for small angles.
    These systems are found in various applications, such as timekeeping in clocks and watches, and in musical instruments where vibrating strings exhibit SHM.
    Understanding SHM is crucial in engineering for designing stable structures.
    Concepts like damping, which causes a gradual decrease in amplitude, and resonance, occurring when an external force matches the natural frequency, are important for analyzing the behavior of oscillatory systems in practical scenarios.

Begin!

Question: {input}
Thought: {agent_scratchpad}
"""
)

agent = initialize_agent(
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    tools=tools,
    llm=llm,
    verbose=True,
    max_iterations=3,
    handle_parsing_errors=True,
)
agent.agent.llm_chain.prompt = fixed_prompt

def main():
    print("Welcome to the AI Assistant!")
    print("You can ask questions, and the AI will try to answer using Tavily AI and DuckDuckGo.")
    print("Type 'quit' to exit the program.")
    print("")
    # print(agent.agent.llm_chain.prompt)
    
    while True:
        question = input("\nEnter your question: ").strip()
        if question.lower() == 'quit':
            print("Thank you for using the AI Assistant. Goodbye!")
            break
        
        try:
            answer = agent.run(input=question, tools=tools)
            print(f"\nAnswer: {answer}")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()



