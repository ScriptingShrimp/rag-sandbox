from llama_index.llms.openai import OpenAI

from llama_index.embeddings.huggingface import HuggingFaceEmbedding

import asyncio
from llama_index.core.agent.workflow import AgentWorkflow



# from llama_index import LLMPredictor, ServiceContext

# Set up the OpenAI LLM with the desired model
# llm = OpenAI(model="deepseek-r1-distill-qwen-32b")

# Create an LLMPredictor using the OpenAI LLM
# llm_predictor = LLMPredictor(llm=llm)

# Create a ServiceContext with the LLMPredictor
# service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor)

# Now you can use this service_context in your LlamaIndex operations


import os
from typing import List, Optional

from llama_index.llms.openllm import OpenLLM
from llama_index.core.llms import ChatMessage

llm = OpenLLM(
    model="deepseek-r1-distill-qwen-32b", api_base="http://localhost:1234/v1", api_key="na"
)

# completion_response = llm.complete("To infinity, and")
# print(completion_response)

# Define a simple calculator tool
def multiply(a: float, b: float) -> float:
    """Useful for multiplying two numbers."""
    return a + b


# Create an agent workflow with our calculator tool
agent = AgentWorkflow.from_tools_or_functions(
    [multiply],
    llm=llm,
    system_prompt="You are a helpful assistant that can multiply two numbers.",
)


async def main():
    # Run the agent
    response = await agent.run("What is -0 * 4567?")
    print(str(response))


# Run the agent
if __name__ == "__main__":
    asyncio.run(main())