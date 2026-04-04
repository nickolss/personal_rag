from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage

from config.settings import get_groq_api_key


def create_llm(model: str = "qwen/qwen3-32b", temperature: float = 0, reasoning_effort: str = "none"):
    api_key = get_groq_api_key()
    
    llm = ChatGroq(
        model=model,
        temperature=temperature,
        max_tokens=None,
        timeout=None,
        max_retries=3,
        api_key=api_key,
        reasoning_effort=reasoning_effort,
    )
    return llm


def create_system_prompt() -> list:
    personality = open("./personality.txt", "r").read()

    return [
        SystemMessage(content=personality)
    ]


def ask_llm(llm, messages: list, user_input: str = None):
    if user_input:
        messages.append(HumanMessage(content=user_input))
    
    result = llm.invoke(messages)
    return result
