import psycopg2
import yaml
import logging
import sys

from llama_index.core import SimpleDirectoryReader, StorageContext, VectorStoreIndex
from llama_index.core.schema import TextNode
from llama_index.vector_stores.postgres import PGVectorStore
from llama_index.embeddings.ollama import OllamaEmbedding
from psycopg2 import sql
from typing import List


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

# Load YAML config
with open("config.yaml") as f:
    cfg = yaml.safe_load(f)


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
    CREATE EXTENSION IF NOT EXISTS vector;
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

# Load your documents
reader = SimpleDirectoryReader(
    input_dir=cfg["data"]["folder"],
    required_exts=cfg["data"]["extensions"],
    recursive=True,
)

docs = reader.load_data()
print(f"Loaded {len(docs)} docs")


print("PGVectorStore initialized")
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

# Generate embeddings
embeddings = embed_model.get_text_embedding_batch(
    [doc.text for doc in docs], show_progress=True
)

# Create list of TextNode objects with embeddings and text
nodes: List[TextNode] = []
for doc_text, embedding in zip(docs, embeddings):
    node = TextNode(text=doc_text.text, embedding=embedding,)
    nodes.append(node)

# Create the index from nodes
index = VectorStoreIndex(nodes, embed_model=embed_model, storage_context=storage_context)

# Persist the index to PostgreSQL
index.storage_context.persist()















# # Define your ingestion pipeline
# pipeline = IngestionPipeline(transformations=[embed_model])

# # Convert documents to Node objects
# nodes = [Node(document=Document(text=doc.text, metadata={"id": f"doc_{i}"})) for i, doc in enumerate(docs)]

# # Run the pipeline to process nodes and generate embeddings
# processed_nodes = pipeline.run(nodes)


# index = VectorStoreIndex(processed_nodes, embed_model=embed_model, storage_context=storage_context)

# # index.storage_context.persist(persist_dir="/path/to/storage")


# Insert processed nodes into your custom vector store
# vector_store.insert(processed_nodes)

# Now your custom vector store contains the documents and their embeddings

















# pass_embedding = embed_model.get_text_embedding_batch(
#     ["This is a passage!", "This is another passage"], show_progress=True
# )
# print(pass_embedding)

# query_embedding = embed_model.get_query_embedding("Where is blue?")
# print(query_embedding)

# index = VectorStoreIndex.from_documents(
#     docs,
#     embed_model=embed_model,
#     storage_context=storage_context,
#     show_progress=True,
#     )

# # # Create and store the index  Build the index with your documents
# index = VectorStoreIndex.from_documents(
#     docs, embed_model=embed_model, storage_context=storage_context
# )

# # Persist the index to PostgreSQL
# index.storage_context.persist()