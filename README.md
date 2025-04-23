# rag-sandbox
Run your own naive RAG locally!

# setup 
## requirements 
ollama, podman, python3.12
```
$ ollama pull mxbai-embed-large:latest
$ ollama pull granite3.3:latest

# linux (use python3.12 binary)
$ /usr/bin/python3.12 -m venv ./venv
# or MacOS
$/Library/Frameworks/Python.framework/Versions/3.12/bin/python3.12 -m venv ./venv

$ source ./venv/bin/activate
$ pip install -r requirements.txt

$ podman play kube pods.yaml

$ cd ./data/repos 
$ git clone git@github.com:kiali/kiali.git && git clone git@github.com:istio-ecosystem/sail-operator.git 
```

## usage
- after setup run `python embeddings.py`
- once you emmbed all your documents, you can check via pgadmin at `localhost:8888` - see `pods.yaml` line 19 for credentials
- you needo to register your pgvector
- ![image](https://github.com/user-attachments/assets/12860396-f137-4c23-ba85-5785ccafcd84)
- embeddings are stored in mydatabase > schemas > tables > data_ossm30 (rightclick "View/Edit Data")
- run `python naive-rag.py` to answer generic question or change it via `response = query_engine.query("what is sail operator and how to use it?")`
- check `config.yaml` for additional variables 

## TODO
- flag to diable debugging output
- pass `pgsql.json` to pods on creation / setup
