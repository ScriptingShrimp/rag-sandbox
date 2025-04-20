from sqlalchemy import create_engine
from llama_index.core import StorageContext
from llama_index.vector_stores.postgres import PGVectorStore
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.embeddings.ollama import OllamaEmbedding
from sqlalchemy import create_engine
from llama_index.llms.ollama import Ollama
import yaml
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

# Load YAML config
with open("config.yaml") as f:
    cfg = yaml.safe_load(f)

# Initialize Ollama LLM
llm = Ollama(
    model=cfg['ollama']['model'],
    request_timeout=360.0,
    temperature=cfg['ollama']['temperature'],
    )
# Select an embedding model
embed_model = OllamaEmbedding(model_name=cfg['embedding']['model'])

# Create a connection string
connection_string = f"postgresql://(user):{cfg["db"]["password"]}@{cfg["db"]["host"]}:{cfg["db"]["port"]}/{cfg["db"]["name"]}"

# Initialize PGVectorStore
vector_store = PGVectorStore.from_params(
    database=cfg["db"]["name"],
    user=cfg["db"]["user"],
    password=cfg["db"]["password"],
    host=cfg["db"]["host"],
    port=cfg["db"]["port"],
    table_name=cfg["db"]["table"],
    embed_dim=cfg["embedding"]["dimensions"]
)

# Create a storage context with the existing vector store
storage_context = StorageContext.from_defaults(vector_store=vector_store)

# Load the index from the storage context
index = VectorStoreIndex.from_vector_store(
    vector_store, 
    embed_model=embed_model, 
    storage_context=storage_context,
)

# Create a query engine
query_engine = index.as_query_engine(llm=llm)
# Query the index
response = query_engine.query("how I can create server to serve llamaindex RAG? ")
print(response)
