###################################################################################################
# Image captioning agent that first downloads image and then gives captions, inputting query by user
###################################################################################################
import os
from dotenv import load_dotenv
from PIL import Image
import google.generativeai as genai
from langchain_community.llms import HuggingFaceEndpoint
from langchain.agents import AgentExecutor, BaseSingleActionAgent
from langchain.memory import ConversationBufferMemory
from langchain.schema import AgentFinish
from icrawler.builtin import BingImageCrawler
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

def GeminiVision(): 
    model = genai.GenerativeModel('gemini-pro-vision')
    return model

def GenerateImageCaption(image_path):
    try:
        model = GeminiVision()
        image = Image.open(image_path)
        prompt = "Generate a detailed caption for the image, explaining what is happening in the scene. The caption should be easy to understand and informative. Make sure to use LATEX for Mathematical and Numerical equations."            
        response = model.generate_content([prompt, image])
        
        if response.candidates:
            if response.candidates[0].content.parts:
                return response.text
            else:
                safety_ratings = response.candidates[0].safety_ratings
                return f"Caption generation blocked due to safety concerns: {safety_ratings}"
        else:
            return "Caption generation failed: No valid response from the model."
    except Exception as e:
        return f"Caption generation failed: {str(e)}"

def DownloadImages(keyword, max_num=1):
    try:
        google_crawler = BingImageCrawler(storage={'root_dir': f'./images/{keyword}'})
        google_crawler.crawl(keyword=keyword, max_num=max_num)
        return True
    except Exception as e:
        print(f"Error downloading image: {str(e)}")
        return False

def ExtractKeyword(query):
    # Use the LLM to extract the keyword from the natural language query
    prompt = f"Extract the main (correctly spelled) keyword for image search from this query: '{query}'. Return only the keyword, nothing else."
    return llm(prompt).strip()

class ImageCaptionAgent(BaseSingleActionAgent):
    def plan(
        self, intermediate_steps: List[Tuple[Any, str]], **kwargs: Any
    ) -> Union[Any, AgentFinish]:
        query = kwargs["input"]
        keyword = ExtractKeyword(query)
        
        download_success = DownloadImages(keyword, max_num=1)
        
        if not download_success:
            return AgentFinish(
                return_values={"output": f"I'm sorry, I couldn't find any images for '{keyword}'. Could you try a different query?"},
                log=f"Failed to download image for keyword: {keyword}"
            )
        
        image_path = f'./images/{keyword}/'

        image_file = None
        for ext in ['.jpg', '.png', '.jpeg', '.gif']:
            if os.path.isfile(image_path + '000001' + ext):
                image_file = '000001' + ext
                break

        if image_file:
            full_image_path = image_path + image_file
            caption = GenerateImageCaption(full_image_path)
            
            if caption.startswith("Caption generation failed") or caption.startswith("Caption generation blocked"):
                return AgentFinish(
                    return_values={
                        "output": f"I found an image for '{keyword}', but I couldn't generate a caption for it. Here's what happened: {caption}"
                    },
                    log=f"Downloaded image but failed to generate caption for keyword: {keyword}"
                )
            else:
                return AgentFinish(
                    return_values={
                        "output": f"I found an image for '{keyword}'!\n\nImage: {full_image_path}\n\nHere's what I see: {caption}"
                    },
                    log=f"Downloaded image and generated caption for keyword: {keyword}"
                )
        else:
            return AgentFinish(
                return_values={"output": f"I'm sorry, I couldn't find any suitable images for '{keyword}'. Could you try a different query?"},
                log=f"No suitable image file found for keyword: {keyword}"
            )

    async def aplan(
        self, intermediate_steps: List[Tuple[Any, str]], **kwargs: Any
    ) -> Union[Any, AgentFinish]:
        return self.plan(intermediate_steps, **kwargs)

    @property
    def input_keys(self):
        return ["input"]

agent = ImageCaptionAgent()
agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent,
    tools=[],
    verbose=True,
    memory=ConversationBufferMemory(memory_key="chat_history")
)

def ProcessQuery(query):
    return agent_executor.run(query)

if __name__ == "__main__":
    while True:
        query = input("Enter your query: ")
        result = ProcessQuery(query)
        print(result)
        print("\n-----------------------------------------------")