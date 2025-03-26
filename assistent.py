from sqlalchemy import create_engine
from llama_index.core import StorageContext
from llama_index.vector_stores.postgres import PGVectorStore
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from sqlalchemy import create_engine
from llama_index.llms.ollama import Ollama

# Initialize Ollama LLM
llm = Ollama(model="llama3.3:70b-instruct-q2_K", request_timeout=360.0)


embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")
# Database connection details
db_name = "mydatabase"
host = "localhost"
user = "admin"
password = "secret"
port = "5432"

# Create a connection string
connection_string = f"postgresql://(user):{password}@{host}:{port}/{db_name}"

# Initialize PGVectorStore
vector_store = PGVectorStore.from_params(
    database=db_name,
    host=host,
    password=password,
    port=port,
    user=user,
    table_name="vector_store_table",
    embed_dim=384  # Example embedding dimension
)


# Create a storage context with the existing vector store
storage_context = StorageContext.from_defaults(vector_store=vector_store)
# Load the index from the storage context
index = VectorStoreIndex.from_vector_store(vector_store, embed_model=embed_model, storage_context=storage_context)

# Create a query engine
query_engine = index.as_query_engine(llm=llm)
# Query the index
response = query_engine.query("how to setup and test kiali in kind cluster?")
print(response)



# Use the LLM to generate responses based on retrieved context
llm_response = llm.complete(response)
print(llm_response)
