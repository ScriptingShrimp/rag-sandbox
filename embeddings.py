from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext
)
from llama_index.vector_stores.postgres import PGVectorStore
from llama_index.embeddings.ollama import OllamaEmbedding

import psycopg2
from psycopg2 import sql
import yaml

import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

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
embed_model = OllamaEmbedding(
    model_name=cfg["embedding"]["model"],
    max_length=cfg["embedding"]["dimensions"],
    base_url="http://localhost:11434",
    embed_batch_size=1024,
    ollama_additional_kwargs={"mirostat": 0},
    )





pass_embedding = embed_model.get_text_embedding_batch(
    ["This is a passage!", "This is another passage"], show_progress=True
)
print(pass_embedding)

query_embedding = embed_model.get_query_embedding("Where is blue?")
print(query_embedding)




index = VectorStoreIndex.from_documents(
    docs,
    embed_model=embed_model,
    storage_context=storage_context,
    show_progress=True,
    )






# # # Create and store the index  Build the index with your documents
# index = VectorStoreIndex.from_documents(
#     docs, embed_model=embed_model, storage_context=storage_context
# )


# # Persist the index to PostgreSQL
index.storage_context.persist()