# ta
the assistant 

```
$ cd ./data/repos && git clone git@github.com:run-llama/llama_index.git
$ python -m venv ./venv
$ source ./venv/bin/activate
``` 
ollama run llama3.3:70b-instruct-q2_K

curl http://localhost:11434/api/generate -d '{
  "model": "llama3.3:70b-instruct-q2_K",
  "prompt": "Why is the sky blue? give me short answer"
}'

## example answer:

 user question: 
 I want to build a simple Retrieval Augmented Generation (RAG) but my knowledge of coding is limited. I want to leverage llamaindex library and as a first steps I want to: 
 - crate Loading from files on the disk 
 - index files loaded from the disk 
 - store loaded data into pgsql 

To create a simple Retrieval Augmented Generation (RAG) using the llamaindex library, you'll need to follow these steps. This guide will walk you through loading data from files, indexing it, and storing the indexed data in PostgreSQL.

### Step 1: Setting Up Your Environment

First, ensure you have Python installed on your system. You'll also need to install the `llamaindex` library and a PostgreSQL database for storage. 

- **Install Python**: If you haven't already, download and install Python from [python.org](https://www.python.org/).
- **Install llamaindex**: Use pip to install the llamaindex library. As of my last update, you can install it directly using pip (if available) or by installing from a source repository if it's not available on PyPI:
  ```bash
  pip install llamaindex
  ```
- **PostgreSQL Installation**:
  - For Windows and macOS: Download and install PostgreSQL from the [official website](https://www.postgresql.org/download/).
  - For Linux (Ubuntu-based distributions as an example): 
    ```bash
    sudo apt update
    sudo apt install postgresql postgresql-contrib
    ```
- **Python Library for PostgreSQL**: Install the `psycopg2` library to interact with PostgreSQL databases:
  ```bash
  pip install psycopg2
  ```

### Step 2: Loading Data from Files

For this example, let's assume you have text files containing information you want to index. Create a Python script that loads these files:

```python
import os

def load_data_from_disk(directory_path):
    loaded_data = []
    for filename in os.listdir(directory_path):
        if filename.endswith(".txt"):  # Assuming text files only
            file_path = os.path.join(directory_path, filename)
            try:
                with open(file_path, 'r') as file:
                    content = file.read()
                    loaded_data.append((filename, content))
            except Exception as e:
                print(f"Failed to load {filename}: {e}")
    return loaded_data

# Example usage
directory_path = '/path/to/your/files'
loaded_data = load_data_from_disk(directory_path)
print(loaded_data)
```

### Step 3: Indexing the Loaded Data

Indexing in the context of RAG typically refers to preparing the data for querying or generation. The `llamaindex` library might offer functionalities for this purpose, but since its specifics are not detailed here, we'll focus on a generic approach to structure your data:

```python
import llamaindex  # Import the llamaindex library

def index_loaded_data(loaded_data):
    indexed_data = []
    for filename, content in loaded_data:
        # Assuming llamaindex has a function to prepare or index the data
        indexed_content = llamaindex.prepare(content)  # Example method
        indexed_data.append((filename, indexed_content))
    return indexed_data

# Continue from previous step
indexed_data = index_loaded_data(loaded_data)
print(indexed_data)
```

### Step 4: Storing Indexed Data in PostgreSQL

To store the indexed data, you'll first need to create a table in your PostgreSQL database. Then, use Python's `psycopg2` library to insert the data:

```python
import psycopg2

def store_indexed_data_in_postgresql(indexed_data, db_host, db_name, db_user, db_password):
    try:
        # Establish a connection
        conn = psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host=db_host
        )
        cur = conn.cursor()
        
        # Create table if not exists (example schema)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS indexed_data (
                id SERIAL PRIMARY KEY,
                filename VARCHAR(255),
                indexed_content TEXT
            );
        """)
        
        # Insert data
        for filename, content in indexed_data:
            cur.execute("INSERT INTO indexed_data (filename, indexed_content) VALUES (%s, %s);", (filename, content))
        
        conn.commit()
        print("Data stored successfully.")
    except psycopg2.Error as e:
        print(f"Error storing data: {e}")
    finally:
        if conn:
            cur.close()
            conn.close()

# Example connection parameters
db_host = 'localhost'
db_name = 'your_database'
db_user = 'your_username'
db_password = 'your_password'

store_indexed_data_in_postgresql(indexed_data, db_host, db_name, db_user, db_password)
```

### Conclusion

This guide provides a basic framework for loading data from files, indexing it (with the assumption of using `llamaindex` library functions), and storing the indexed data in PostgreSQL. Adjust the specifics according to your project's needs and the actual functionalities provided by the `llamaindex` library.