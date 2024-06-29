import os
from dotenv import load_dotenv
from langchain.llms import HuggingFaceEndpoint
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
    
    def generate_code(self, prompt: str) -> str:
        # Use the LLM to generate code based on the prompt
        response = self.llm.invoke(prompt)
        return response

    def create_test_function(self, code: str) -> str:
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

    def test_code(self, test_code: str) -> None:
        # Write the test code to a temporary file
        with open("test_generated_code.py", "w") as f:
            f.write(test_code)
        
        # Run the test file using unittest
        os.system("python test_generated_code.py")

    def run(self, prompt: str) -> str:
        # Generate code
        code = self.generate_code(prompt)
        
        # Create a test function for the generated code
        test_code = self.create_test_function(code)
        
        # Test the generated code
        self.test_code(test_code)
        
        return code


if __name__ == "__main__":
    load_dotenv()
    api_key = os.getenv("huggingfacehub_api_token")
    agent = AIAgent(
        api_key=api_key,
        repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1",
        temperature=0.8,
        max_length=150
    )
    user_prompt = "Write a Python program to find sum of the first 10 numbers."
    generated_code = agent.run(user_prompt)
    print("Generated Code:\n", generated_code)
