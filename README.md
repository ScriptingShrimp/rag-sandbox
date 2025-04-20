# ta
the assistant 

```
$ ollama pull mxbai-embed-large:latest
$ ollama pull 
$ cd ./data/repos && git clone git@github.com:run-llama/llama_index.git

# for MacOS
$/Library/Frameworks/Python.framework/Versions/3.12/bin/python3.12  -m venv ./venv
# OR linux (use python3.12 binary)
$ python -m venv ./venv
$ source ./venv/bin/activate
$ pip install -r requirements.txt
``` 
ollama run llama3.3:70b-instruct-q2_K

curl http://localhost:11434/api/generate -d '{
  "model": "llama3.3:70b-instruct-q2_K",
  "prompt": "Why is the sky blue? give me short answer"
}'
