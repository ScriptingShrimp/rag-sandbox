# ta
the assistant 

```
$ python -m venv ./venv
$ source ./venv/bin/activate
``` 
ollama run llama3.3:70b-instruct-q2_K

curl http://localhost:11434/api/generate -d '{
  "model": "llama3.3:70b-instruct-q2_K",
  "prompt": "Why is the sky blue? give me short answer"
}'
