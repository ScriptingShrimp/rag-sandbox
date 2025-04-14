from sqlalchemy import create_engine
from llama_index.core import StorageContext
from llama_index.vector_stores.postgres import PGVectorStore
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from sqlalchemy import create_engine
from llama_index.llms.ollama import Ollama
import yaml


# Initialize Ollama LLM
llm = Ollama(model="llama3.3:70b-instruct-q2_K", request_timeout=360.0)

# Load YAML config
with open("config.yaml") as f:
    cfg = yaml.safe_load(f)

# Select an embedding model
embed_model = HuggingFaceEmbedding(model_name=cfg["embedding"]["model"])

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
    storage_context=storage_context)

# Create a query engine
query_engine = index.as_query_engine(llm=llm)
# Query the index
response = query_engine.query("Based on provided context, tell me what is Kiali. Additionaly descripbe Kiali internal API and what is used for?")
print(response)

# Use the LLM to generate responses based on retrieved context
llm_response = llm.complete(response)
print(llm_response)
