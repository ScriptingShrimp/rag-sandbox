import psycopg2
import yaml
import json

from psycopg2 import sql
from psycopg2.extras import Json # Import Json adapter
from llmsherpa.readers import LayoutPDFReader

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
        sentence TEXT,
        meaning TEXT,
        metadata JSONB,
        embedding VECTOR({})
    );
    ''').format(
        sql.Identifier('books'),
        sql.Literal(cfg["embedding"]["dimensions"])
        )
    cursor.execute(create_table_query)
    conn.commit()
    cursor.close()
    conn.close()

create_table_if_not_exists()


llmsherpa_api_url = "http://localhost:5001/api/parseDocument?renderFormat=all"
pdf_url = "/home/scsh/work/github.com/scriptingshrimp/ta/data/books/istio-succinctly.pdf" # also allowed is a file path e.g. /home/downloads/xyz.pdf
pdf_reader = LayoutPDFReader(llmsherpa_api_url)
doc = pdf_reader.read_pdf(pdf_url)


# Establish a persistent connection
conn = psycopg2.connect(
    database=cfg["db"]["name"],
    user=cfg["db"]["user"],
    password=cfg["db"]["password"],
    host=cfg["db"]["host"],
    port=cfg["db"]["port"]
)
cursor = conn.cursor()

for idx in doc.json: 
    if 'sentences' in idx:
        for sentence in idx['sentences']:
            print('sentence', type(sentence))
            print(type(idx)) 
            insert_query = sql.SQL('''
            INSERT INTO {} (sentence, meaning, metadata, embedding)
            VALUES (%s, %s, %s, %s)
            ''').format(sql.Identifier('books'))
            metadata_to_insert = Json(idx) # Use the Json adapter

            cursor.execute(insert_query, (sentence, None, metadata_to_insert, None))


# Commit the transaction
conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()