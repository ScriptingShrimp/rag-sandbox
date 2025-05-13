import yaml
import psycopg2

from psycopg2 import sql
from psycopg2.extras import Json # Import Json adapter
from llama_index.embeddings.ollama import OllamaEmbedding

# Load YAML config
with open("config.yaml") as f:
    cfg = yaml.safe_load(f)

ollama_embedding = OllamaEmbedding(
    model_name=cfg["embedding"]["model"],
    max_length=cfg["embedding"]["dimensions"],    
    base_url="http://localhost:11434",
    ollama_additional_kwargs={"mirostat": 0},
)

# Establish a persistent connection
conn = psycopg2.connect(
    database=cfg["db"]["name"],
    user=cfg["db"]["user"],
    password=cfg["db"]["password"],
    host=cfg["db"]["host"],
    port=cfg["db"]["port"]
)
cursor = conn.cursor()

query_embedding = ollama_embedding.get_query_embedding("Where is blue?")
print(query_embedding)

cursor.execute("SELECT id, sentence FROM books;") # Process only rows without embeddings
rows_to_process = cursor.fetchall()

# print("rows_to_process", rows_to_process)

for row_id, sentence in rows_to_process:
    if sentence: # Ensure sentence is not empty
        try:
            embedding = ollama_embedding.get_text_embedding(sentence)
            update_query = sql.SQL("UPDATE books SET embedding = %s WHERE id = %s")
            cursor.execute(update_query, (embedding, row_id)) # or (Json(embedding), row_id) for JSONB
            conn.commit()
        except Exception as e:
            print(f"Error processing row {row_id}: {e}")
            conn.rollback()
    else:
        print(f"Skipping empty sentence for ID {row_id}.")

print("Finished processing all sentences.")

# query_embedding = ollama_embedding.get_query_embedding("Where is blue?")
# print(query_embedding)

# Close the connection
cursor.close()
conn.close()