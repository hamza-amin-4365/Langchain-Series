import os
from dotenv import load_dotenv
from PIL import Image
import google.generativeai as genai
from langchain.agents import AgentExecutor, BaseSingleActionAgent
from langchain.schema import AgentFinish
from icrawler.builtin import BingImageCrawler
from typing import List, Tuple, Any, Union
import json

load_dotenv()

GOOGLE_API_KEY = os.getenv("Gemini_api_key")

genai.configure(api_key=GOOGLE_API_KEY)

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

class ImageCaptionAgent(BaseSingleActionAgent):
    def plan(
        self, intermediate_steps: List[Tuple[Any, str]], **kwargs: Any
    ) -> Union[Any, AgentFinish]:
        query = kwargs["input"]
        
        download_success = DownloadImages(query, max_num=1)
        
        if not download_success:
            return AgentFinish(
                return_values={"output": json.dumps({
                    "image_path": None,
                    "caption": f"I couldn't find any images for '{query}'. Could you try a different query?"
                })},
                log=f"Failed to download image for query: {query}"
            )
        
        image_path = f'./images/{query}/'

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
                    return_values={"output": json.dumps({
                        "image_path": full_image_path,
                        "caption": f"I found an image, but I couldn't generate a caption for it. Here's what happened: {caption}"
                    })},
                    log=f"Downloaded image but failed to generate caption for query: {query}"
                )
            else:
                return AgentFinish(
                    return_values={"output": json.dumps({
                        "image_path": full_image_path,
                        "caption": caption
                    })},
                    log=f"Downloaded image and generated caption for query: {query}"
                )
        else:
            return AgentFinish(
                return_values={"output": json.dumps({
                    "image_path": None,
                    "caption": f"I couldn't find any suitable images for '{query}'. Could you try a different query?"
                })},
                log=f"No suitable image file found for query: {query}"
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
    verbose=False
)

def ProcessQuery(query):
    result = agent_executor.run(query)
    return json.loads(result)

# Example usage: Run usage.py to see the output
################################################################################################################################
'''

# This snippet uses the Google Generative AI API to generate captions for the images.

import os
from dotenv import load_dotenv
from PIL import Image
import google.generativeai as genai
from langchain.agents import AgentExecutor, BaseSingleActionAgent
from langchain.schema import AgentFinish
from icrawler.builtin import BingImageCrawler
from typing import List, Tuple, Any, Union
import json

load_dotenv('.env.local')

GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")

IMAGE_PATH = "./static/images"

genai.configure(api_key=GOOGLE_API_KEY)

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
        google_crawler = BingImageCrawler(storage={'root_dir': f'{IMAGE_PATH}/{keyword}'})
        google_crawler.crawl(keyword=keyword, max_num=max_num)
        return True
    except Exception as e:
        print(f"Error downloading image: {str(e)}")
        return False

class ImageCaptionAgent(BaseSingleActionAgent):
    def plan(
        self, intermediate_steps: List[Tuple[Any, str]], **kwargs: Any
    ) -> Union[Any, AgentFinish]:
        query = kwargs["input"]
        
        download_success = DownloadImages(query, max_num=1)
        
        if not download_success:
            return AgentFinish(
                return_values={"output": json.dumps({
                    "image_path": None,
                    "caption": f"I couldn't find any images for '{query}'. Could you try a different query?"
                })},
                log=f"Failed to download image for query: {query}"
            )
        
        image_path = f'{IMAGE_PATH}/{query}/'

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
                    return_values={"output": json.dumps({
                        "image_path": full_image_path,
                        "caption": f"I found an image, but I couldn't generate a caption for it. Here's what happened: {caption}"
                    })},
                    log=f"Downloaded image but failed to generate caption for query: {query}"
                )
            else:
                return AgentFinish(
                    return_values={"output": json.dumps({
                        "image_path": full_image_path,
                        "caption": caption
                    })},
                    log=f"Downloaded image and generated caption for query: {query}"
                )
        else:
            return AgentFinish(
                return_values={"output": json.dumps({
                    "image_path": None,
                    "caption": f"I couldn't find any suitable images for '{query}'. Could you try a different query?"
                })},
                log=f"No suitable image file found for query: {query}"
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
    verbose=False,
)

def ProcessQuery(query):
    print(query)
    result = agent_executor.run(query)

    return json.loads(result)
'''