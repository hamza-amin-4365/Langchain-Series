# AI Assistant Repository

This repository contains a collection of Python scripts that implement various AI functionalities, including a chatbot powered by Wikipedia and DuckDuckGo search, a code generation and testing AI, image processing with caption generation, and an image retrieval system. The project utilizes the Langchain framework, Hugging Face models, and various APIs for information retrieval and image processing.

## Features

1. **Chatbot Application (`chatBot.py`)**:
    - An interactive AI tutor that answers questions by searching Wikipedia and DuckDuckGo.
    - Integrates real-time text generation using Hugging Face models.

2. **Code Generation and Testing (`coder.py`)**:
    - An AI agent that can generate Python code based on user prompts.
    - Includes functionality to create test functions for the generated code and run tests to check correctness.

3. **Image Processing and Captioning (`imageProcessing.py`)**:
    - Generates detailed captions for input images using Google's Gemini API.
    - Downloads images from the web based on user queries.

4. **Image Retrieval (`imageRetriever.py`)**:
    - A simple image downloader that retrieves images from Bing based on specified keywords.

5. **Vector Store and Retrieval (`vectorStore.py`)**:
    - Implements a vector store to manage and retrieve documents using embeddings from Hugging Face.
    - Supports question-answering functionality over the stored documents.

6. **Agents for Information Retrieval (`tavilyDdg.py`, `wikiDdgAgent.py`)**:
    - Define agents that utilize Tavily and DuckDuckGo or Wikipedia for answering questions.
    - These agents are designed to assist users in retrieving high-quality information.

## Installation

To set up the project, follow these steps:

1. **Clone the repository**:
    ```bash
    git clone https://github.com/hamza-amin-4365/Langchain-Series.git
    cd Langchain-Series/temp_repo
    ```

2. **Install the required packages**:
    Ensure you have Python installed (preferably Python 3.7 or higher). You can create a virtual environment and install dependencies using pip:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```

3. **Set up environment variables**:
    Create a `.env` file in the root directory of the project and add the following variables:
    ```bash
    huggingfacehub_api_token=YOUR_HUGGINGFACE_API_TOKEN
    Gemin_api_key=YOUR_GOOGLE_GENERATIVE_AI_API_KEY
    TAVILY_API_KEY=YOUR_TAVILY_API_KEY
    ```

4. **Run the applications**:
    - For the Chatbot:
        ```bash
        streamlit run chatBot.py
        ```
    - For the Code Generator:
        ```bash
        python coder.py
        ```
    - For Image Processing:
        ```bash
        python usage.py  # Adjust the usage as necessary based on your needs
        ```
    - For Image Retrieval:
        ```bash
        python imageRetriever.py
        ```

## Usage

- **Chatbot**: Ask questions related to various subjects, and the AI will respond with a combination of Wikipedia and DuckDuckGo results.
- **Code Generation**: Provide a description of what you want to achieve, and the AI will generate the corresponding Python code.
- **Image Processing**: Supply an image, and the AI will generate a descriptive caption for it.
- **Image Retrieval**: Enter a keyword to download related images from Bing.

## Contributing

Contributions are welcome! If you have suggestions or improvements, please feel free to submit a pull request. Make sure to follow the coding standards and include tests for your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

This README provides an overview of the capabilities and functionality of the AI Assistant repository. For further details about each script, please refer to the respective source files.
