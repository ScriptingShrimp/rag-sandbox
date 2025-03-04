from ollama import chat
from ollama import ChatResponse
from llama_index.core import SimpleDirectoryReader

documents = SimpleDirectoryReader("./data").load_data()

response: ChatResponse = chat(model='llama3.3:70b-instruct-q2_K', messages=[
  {
    'role': 'user',
    'content': 'Why is the sky blue? Give me super short answer.',
  },
])


print(response['message']['content'])
# or access fields directly from the response object
print(response.message.content)

