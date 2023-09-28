from langchain.chains.router import MultiPromptChain
from langchain.llms import OpenAI
from bot import conversation_chain, llm_chain


prompt_info = [
    {
        "name": "qa_chain",
        "description": "Greeting template, conversational guardrail template",
        "prompt_template": llm_chain
    },
    {
        "name": "conversation_chain",
        "description": "Conversational template, memory chat history",
        "prompt_template": conversation_chain
    },
]

for p_info in prompt_info:
    name = p_info["name"]
    prompt_template = p_info["prompt_template"]
    