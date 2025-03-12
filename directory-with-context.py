from ollama import chat
from ollama import ChatResponse
from llama_index.core import SimpleDirectoryReader

# only load markdown files
required_exts = [".md", ".ipynb", ".py"]

reader = SimpleDirectoryReader(
    input_dir="./data/repos/llama_index",
    required_exts=required_exts,
    recursive=True,
)

docs = reader.load_data()
print(f"Loaded {len(docs)} docs")

aggregate_scripts = ''

for doc in docs:
  aggregate_scripts += doc.text
# print(aggregate_scripts)

systemprompt = 'You are a knowledgeable, efficient, and direct Al assistant. Provide concise answers, focusing on the key information needed. Offer suggestions tactfully when appropriate to improve outcomes. Engage in productive collaboration with the user utilising multi-step reasoning to answer the question, if there are multiple questions in the initial question split them up and answer them in the order that will provide the most accurate response. \n',
context = 'This context is needed for an assistant to help answer the question correctly. When answering, uitilize provided context to give specific examples. If the examples in the provided context could be better suited to the user needs, modify the examples to fit the need of the user. \n Now follows the context:',
question = 'I want to build a simple Retrieval Augmented Generation (RAG) but my knowledge of coding is limited. I want to leverage llamaindex library and as a first steps I want to: \n - crate Loading from files on the disk \n - index files loaded from the disk \n - store loaded data into pgsql \n'

content = 'system prompt: \n  {0} \n context needed for answer: \n {1} \n {2} \n user question: \n {3}'.format(systemprompt, context, aggregate_scripts, question)

response: ChatResponse = chat(model='llama3.3:70b-instruct-q2_K', messages=[
  {
    'role': 'user',
    # 'content': 'Help me write new testcase in cypress for a kiali. test case should respect existing form and functions. It should be atomic and test only one thing using BDD approach as it is in examples. The test and sceanrio needs to verify if control plane informations are dispalyed in mesh page view. use only already existing codebase and fuctions and nothing else',
    # 'content': 'based on following provided context: \n\n' + aggregate_scripts + ' \n\n create an llamaindex agent who is capable to search web and answer questions using web search' 
    'content': content
  },
])


print(response['message']['content'])

