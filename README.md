# Spotify and Mpesa RAG Agent

This project demonstrates the use of Retrieval-Augmented Generation (RAG) with Large Language Models (LLMs) using the Ollama framework. It includes scripts for creating embeddings from Spotify CSV data and Mpesa PDF statements, and querying them.

## Requirements

- Python 3.10 or later
- Ollama installed and running locally
- Mistral model and `nomic-embed-text:latest` embedding installed

## Installation

1. **Clone the repository:**

    ```sh
    git clone https://github.com/yourusername/spotify-mpesa-rag-agent.git
    cd spotify-mpesa-rag-agent
    ```

2. **Create and activate a virtual environment:**

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required Python dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

## Setting Up Ollama

1. Ensure Ollama is installed and running locally. Installation instructions can be found [here](https://ollama.ai/docs/installation).

2. **Install the required models:**

    ```sh
    ollama install gemma
    ollama install mistral
    ollama install nomic-embed-text:latest
    ```

3. **Start Ollama server:**

    ```sh
    ollama serve
    ```

## Running the Database Scripts

1. **Populate the Spotify database:**

    ```sh
    python populate_spotifydb.py --reset
    ```

2. **Populate the Mpesa database:**

    ```sh
    python populate_mpesadb.py --reset
    ```

## Running the Query Scripts

1. **Query the Spotify database:**

    ```sh
    python query_data.py "Which artist is the most listened to?"
    ```

2. **Query the Mpesa database:**

    ```sh
    python query_data.py "What is my total expenditure?"
    ```

## Notes

- Ensure your data files (Spotify CSV and Mpesa PDF statements) are placed in the `data` directory.
- The `--reset` flag in the database scripts clears the existing database before populating it with new data.
- Inspired by pixegami

## License

This project is licensed under the MIT License.
