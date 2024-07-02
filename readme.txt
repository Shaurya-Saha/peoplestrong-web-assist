# PeopleStrong Web Assitant

## Overview
The PeopleStrong Assistant is an intelligent chatbot designed to assist users visiting the PeopleStrong website. It leverages OpenAI's LLM to provide insightful and helpful answers to user queries. The system employs ChromaDB as the VectorStore and performs Retrieval-Augmented Generation (RAG) over data scraped from PeopleStrong's public website.

## Features
- **OpenAI LLM**: Utilizes OpenAI's powerful language model to generate responses.
- **ChromaDB**: Stores and retrieves vector representations of the scraped data.
- **RAG**: Performs Retrieval-Augmented Generation to provide accurate and context-aware answers.
- **User Assistance**: Acts as a helpful assistant, answering questions and providing information to website visitors via a chatbot interface.

## Files
### `create_rag.py`
This script is responsible for creating the RAG system using ChromaDB and Langchain. It processes the scraped data, generates vector embeddings, and stores them in ChromaDB for efficient retrieval.

### `run_rag.py`
This script sets up and runs the chatbot using the Gradio UI. It showcases the chatbot in action, allowing users to interact with the assistant and receive helpful responses to their queries.

## Getting Started
1. **Clone the Repository**:
    ```sh
    git clone https://github.com/Shaurya-Saha/peoplestrong-web-assist.git
    cd peoplestrong-web-assist
    ```

2. **Install Dependencies**:
    ```sh
    pip install -U pip
    pip install langchain langchain_community langchain_openai chromadb pypdf PyMuPdf gradio pillow
    ```

3. Setup the following environment variables:
   PROJECT_ROOT
   OPENAI_API_KEY

4. **Create the RAG**:
    - Run the `create_rag.py` script to generate the RAG system.
    ```sh
    python create_rag.py
    ```

5. **Run the Chatbot**:
    - Launch the chatbot using Gradio by running the `run_rag.py` script.
    ```sh
    python run_rag.py
    ```

6. **Interact with the Chatbot**:
    - Open the provided Gradio UI link in your browser.
    - Ask questions and receive answers from the PeopleStrong Assistant.

Note: This is a PyCharm project so you can directly open the project in PyCharm and run the scripts from there.

## License
This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Contributing
We welcome contributions! Please fork the repository and create a pull request with your changes.