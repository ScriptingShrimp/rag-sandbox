from llama_index.core import SimpleDirectoryReader
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.postgres import PGVectorStore
from llama_index.core import StorageContext, VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
import psycopg2
from psycopg2 import sql
import yaml

# Load YAML config
with open("config.yaml") as f:
    cfg = yaml.safe_load(f)

# Load your documents
reader = SimpleDirectoryReader(
    input_dir=cfg["data"]["folder"],
    required_exts=cfg["data"]["extensions"],
    recursive=True,
)

docs = reader.load_data()
print(f"Loaded {len(docs)} docs")

def create_table_if_not_exists():
    conn = psycopg2.connect(
        database=cfg["db"]["name"],
        user=cfg["db"]["user"],
        password=cfg["db"]["password"],
        host=cfg["db"]["host"],
        port=cfg["db"]["port"]
    )

    cursor = conn.cursor()
    create_table_query = sql.SQL('''
    CREATE TABLE IF NOT EXISTS {} (
        id SERIAL PRIMARY KEY,
        text TEXT NOT NULL,
        metadata JSONB,
        embedding VECTOR({})
    );
    ''').format(
        sql.Identifier(cfg["db"]["table"]),
        sql.Literal(cfg["embedding"]["dimensions"])
        )
    cursor.execute(create_table_query)
    conn.commit()
    cursor.close()
    conn.close()


# Create the table if it does not exist
create_table_if_not_exists()

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
# Create a storage context with the PGVectorStore
storage_context = StorageContext.from_defaults(vector_store=vector_store)

# Select an embedding model
embed_model = HuggingFaceEmbedding(
    model_name=cfg["embedding"]["model"],
    # max_length=cfg["embedding"]["dimensions"]
    )

# Create and store the index  Build the index with your documents
index = VectorStoreIndex.from_documents(
    docs,
    embed_model=embed_model,
    storage_context=storage_context
    )

# Persist the index to PostgreSQL
index.storage_context.persist()