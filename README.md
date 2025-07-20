# About the project
**DocTech IA** is an _open-source_ project focused on the automatic generation of technical documentation through source code analysis. Its operation is inspired by tools such as _Deep Wiki_ and is designed to analyze a cloned repository from its root directory, recursively traversing all its files and subdirectories.

The project code is fragmented and transformed into _embeddings_, which are used by a language model (LLM) to understand the repository's content. With this information, the model generates accurate and coherent technical documentation, closely aligned with the logic and structure of the code.

DocTech IA will be compatible with locally executed LLM models, such as those supported by Ollama or LM Studio, as well as with models accessible via APIs, such as **OpenAI's ChatGPT** or **Google's Gemini**.

The project is developed in **Python 3.10 or higher**.

You need to create a `.env` file 

```env
LLM_PROVIDER="ollama"  
EMBEDDING_PROVIDER="ollama"  

# DEFAULT: Add this if you want to use Ollama models
OLLAMA_BASE_URL="http://localhost:11434" 
GOOGLE_API_KEY="YOUR_GOOGLE_API_KEY" 
OPENAI_API_KEY="YOUR_OPENAI_API_KEY"

OLLAMA_MODEL="qwen2.5-coder:3b"
OPENAI_MODEL="YOUR_SELECTED_MODEL"  
GOOGLE_MODEL="YOUR_SELECTED_MODEL"

OLLAMA_EMBEDDING_MODEL="nomic-embed-text"  
OPENAI_EMBEDDING_MODEL="text-embedding-3-small"
DIMENSION_EMBEDDING_DIMENSION=768

POSGRESQL_DB_NAME="YOUR_DATABASE_NAME_POSGRESQL"
POSGRESQL_DB_USER="YOUR_USER_POSGRESQL"
POSGRESQL_DB_PSW="YOUR_PASSWORD_POSGRESQL"
POSGRESQL_DB_HOST="localhost"
POSGRESQL_DB_PORT="5432"

# ENVIOREMNT CLONING
GITHUB_TOKEN="YOUR_TOKEN_GITHUB"
```
