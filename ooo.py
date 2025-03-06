from ollama import chat
from ollama import ChatResponse
from llama_index.core import SimpleDirectoryReader

# only load markdown files
required_exts = [".sh"]

reader = SimpleDirectoryReader(
    input_dir="./data/repos/kiali-master",
    required_exts=required_exts,
    recursive=True,
)

docs = reader.load_data()
print(f"Loaded {len(docs)} docs")

aggregate_scripts = ''

for doc in docs:
  aggregate_scripts += doc.text

print(aggregate_scripts)

response: ChatResponse = chat(model='llama3.3:70b-instruct-q2_K', messages=[
  {
    'role': 'user',
    # 'content': 'Help me write new testcase in cypress for a kiali. test case should respect existing form and functions. It should be atomic and test only one thing using BDD approach as it is in examples. The test and sceanrio needs to verify if control plane informations are dispalyed in mesh page view. use only already existing codebase and fuctions and nothing else',
    'content': 'suggest best practicies in probided context of bash scripts: ' + aggregate_scripts  
  },
])


print(response['message']['content'])

