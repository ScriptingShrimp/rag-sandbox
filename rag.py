from llama_index.core import SimpleDirectoryReader
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.postgres import PGVectorStore
from llama_index.core import StorageContext, VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
import psycopg2

# Initialize PostgreSQL connection parameters
db_params: dict[str, str | int] = {
    'database': 'mydatabase',
    'user': 'admin',
    'password': 'secret',
    'host': 'localhost',
    'port': 5432
}


def create_table_if_not_exists():
    conn = psycopg2.connect(
        database=db_params['database'],
        user=db_params['user'],
        password=db_params['password'],
        host=db_params['host'],
        port=db_params['port']
    )
    cursor = conn.cursor()
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS vector_store_table (
        id SERIAL PRIMARY KEY,
        text TEXT NOT NULL,
        metadata JSONB,
        embedding VECTOR(384)
    );
    '''
    cursor.execute(create_table_query)
    conn.commit()
    cursor.close()
    conn.close()


# Create the table if it does not exist
create_table_if_not_exists()

# Initialize PGVectorStore
vector_store = PGVectorStore.from_params(
    database=db_params['database'],
    user=db_params['user'],
    password=db_params['password'],
    host=db_params['host'],
    port=db_params['port'],
    table_name='vector_store_table',  # Ensure this table exists
    embed_dim=384  # Updated embedding dimension
)
# Create a storage context with the PGVectorStore
storage_context = StorageContext.from_defaults(vector_store=vector_store)
# Load your documents
# documents = [...]  # Replace with your document loading logic
# Choose an embedding model
# embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")


# only load bash and markdown files
required_exts = [".md", ".sh"]

reader = SimpleDirectoryReader(
    input_dir="./data/repos/kiali-master",
    required_exts=required_exts,
    recursive=True,
)

docs = reader.load_data()
print(f"Loaded {len(docs)} docs")

# Select an embedding model
embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Create and store the index  Build the index with your documents
index = VectorStoreIndex.from_documents(docs, embed_model=embed_model, storage_context=storage_context)
# Persist the index to PostgreSQL
index.storage_context.persist()