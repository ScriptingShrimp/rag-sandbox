# rag-sandbox
Run your own naive RAG locally!

```
$ ollama pull mxbai-embed-large:latest
$ ollama pull granite3.3:latest
$ cd ./data/repos 
$ git clone git@github.com:kiali/kiali.git && git clone git@github.com:istio-ecosystem/sail-operator.git 


# linux (use python3.12 binary)
$ /usr/bin/python3.12 -m venv ./venv
# or MacOS
$/Library/Frameworks/Python.framework/Versions/3.12/bin/python3.12 -m venv ./venv

$ source ./venv/bin/activate
$ pip install -r requirements.txt

$ podman play kube pods.yaml
``` 

TODO: pass `pgsql.json` to pods on creation / setup
