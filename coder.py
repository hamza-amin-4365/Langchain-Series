#######################################################
# Coder LLM that can generate and test code
#######################################################
import os
import re
from dotenv import load_dotenv
from langchain.llms import HuggingFaceEndpoint
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import unittest

class AIAgent:
    def __init__(self, api_key: str, repo_id: str, temperature: float = 0.8, max_length: int = 150):
        # Initialize the HuggingFace LLM endpoint
        self.llm = HuggingFaceEndpoint(
            huggingfacehub_api_token=api_key,
            repo_id=repo_id,
            temperature=temperature,
            max_length=max_length
        )

    def GenerateCode(self, prompt: str) -> str:
        # Use the LLM to generate code based on the prompt
        response = self.llm.invoke(prompt)
        return response

    def CreateTestFunction(self, code: str) -> str:
        # Simple test function creation (This should be more sophisticated)
        test_code = f"""
import unittest

class TestGeneratedCode(unittest.TestCase):
    def test_code(self):
        # Import the generated code
        exec(\"\"\"
{code}
        \"\"\")
        # Add specific test cases here
        self.assertTrue(True)  # Placeholder assertion

if __name__ == "__main__":
    unittest.main()
"""
        return test_code

    def TestCode(self, code: str) -> bool:
        # Write the code to a temporary file
        with open("generated_code.py", "w") as f:
            f.write(code)
        
        # Write the test code
        test_code = self.CreateTestFunction(code)
        with open("test_generated_code.py", "w") as f:
            f.write(test_code)
        
        # Run the test file using unittest and capture the result
        result = os.system("python test_generated_code.py")
        return result == 0

    def ExplainCode(self, code: str) -> str:
        # Use the LLM to generate an explanation of the code
        prompt = f"Explain the following Python code:\n{code}"
        explanation = self.llm.invoke(prompt)
        return explanation

    def FixCode(self, code: str, error_message: str) -> str:
        # Use the LLM to fix the code based on the error message
        prompt = f"Fix the following Python code:\n{code}\nError message: {error_message}"
        fixed_code = self.llm.invoke(prompt)
        return fixed_code

    def run(self, input_text: str) -> str:
        if self.IsCode(input_text):
            # If input is code, validate and correct it
            code = input_text
            while True:
                if self.TestCode(code):
                    break
                else:
                    error_message = self.GetErrorMessage()
                    code = self.FixCode(code, error_message)
            explanation = self.ExplainCode(code)
            return f"Corrected Code:\n{code}\n\nExplanation:\n{explanation}"
        else:
            # If input is natural language, generate code
            code = self.GenerateCode(input_text)
            return f"Generated Code:\n{code}"

    def IsCode(self, text: str) -> bool:
        # Check if the input text looks like a code snippet
        return bool(re.search(r'\bdef\b|\bclass\b|\bimport\b', text))

    def GetErrorMessage(self) -> str:
        # Extract the last error message from the test run
        with open("test_generated_code.py", "r") as f:
            lines = f.readlines()
        error_message = ""
        for line in reversed(lines):
            if "Traceback" in line or "Error" in line:
                error_message = line + error_message
            elif error_message:
                error_message = line + error_message
        return error_message

if __name__ == "__main__":
    load_dotenv()
    api_key = os.getenv("huggingfacehub_api_token")
    agent = AIAgent(
        api_key=api_key,
        repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1",
        temperature=0.8,
        max_length=150
    )
    user_input = input("Enter your query or code: ")
    result = agent.run(user_input)
    print(result)
