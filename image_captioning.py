import os
from dotenv import load_dotenv
from PIL import Image
import google.generativeai as genai
from langchain_community.llms import HuggingFaceEndpoint
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.agents import Tool, AgentExecutor, BaseSingleActionAgent
from langchain.memory import ConversationBufferMemory
from langchain.schema import AgentAction, AgentFinish
from typing import List, Tuple, Any, Union

load_dotenv()

GOOGLE_API_KEY = os.getenv("Gemini_api_key")
HUGGINGFACE_API_KEY = os.getenv("huggingfacehub_api_token")

genai.configure(api_key=GOOGLE_API_KEY)

llm = HuggingFaceEndpoint(
    huggingfacehub_api_token=HUGGINGFACE_API_KEY,
    repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1",
    temperature=0.8,
    max_new_tokens=512,
)

def gemini_vision():
    model = genai.GenerativeModel('gemini-pro-vision')
    return model

def generate_image_caption(image_path):
    model = gemini_vision()
    image = Image.open(image_path)
    prompt = "Provide a detailed caption for this image."            
    response = model.generate_content([prompt, image])
    return response.text

template = """You are a friendly and knowledgeable teacher explaining an image to a 10th-grade student.
Given the following image caption, provide an educational and engaging explanation of what the image might depict:

Caption: {caption}

Please explain the image in a way that's easy for a 10th-grade student to understand. Your explanation should:

1. Identify the main subject of the image and its significance.
2. Relate the image to a possible topic or subject they might be studying in school (e.g., biology, history, literature, maths etc.).
3. Explain any scientific, historical, or cultural concepts relevant to the image.
4. Use simple language and avoid jargon, but introduce new vocabulary when appropriate.
5. Include an interesting fact or two related to the subject of the image.
6. Encourage critical thinking by asking a thought-provoking question at the end.

Remember to be enthusiastic and make the explanation engaging for a young learner!

Explanation:"""

prompt = PromptTemplate(
    input_variables=["caption"],
    template=template
)

llm_chain = LLMChain(llm=llm, prompt=prompt)

class ImageExplanationAgent(BaseSingleActionAgent):
    def plan(
        self, intermediate_steps: List[Tuple[AgentAction, str]], **kwargs: Any
    ) -> Union[AgentAction, AgentFinish]:
        image_path = kwargs["input"]
        
        # Generate caption using Gemini Vision
        caption = generate_image_caption(image_path)
        
        # Generate explanation using Hugging Face LLM
        explanation = llm_chain.run(caption=caption)

        return AgentFinish(
            return_values={
                "output": f"Caption: {caption}\n\nExplanation: {explanation}"
            },
            log=f"Generated caption and explanation for image: {image_path}"
        )

    async def aplan(
        self, intermediate_steps: List[Tuple[AgentAction, str]], **kwargs: Any
    ) -> Union[AgentAction, AgentFinish]:
        return self.plan(intermediate_steps, **kwargs)

    @property
    def input_keys(self):
        return ["input"]

# Set up the agent executor
agent = ImageExplanationAgent()
agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent,
    tools=[],  # No tools needed for this simplified version
    verbose=True,
    memory=ConversationBufferMemory(memory_key="chat_history")
)

def process_image(image_path):
    return agent_executor.run(image_path)

if __name__ == "__main__":
    image_path = r'images\Mitochondria\000001.jpg'  # Replace with your image path
    result = process_image(image_path)
    print(result)