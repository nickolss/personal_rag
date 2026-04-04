import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage

from config.settings import get_groq_api_key
from src.chroma import get_chroma_client, create_collection, query_collection


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


def get_context_from_chroma(query, collection_name="documents", n_results=2):
    client = get_chroma_client()
    collection = create_collection(client, collection_name)
    results = query_collection(collection, query, n_results)
    
    if results["documents"] and results["documents"][0]:
        return results["documents"][0][0]
    return None


def ask_with_rag(user_input, context=None):
    llm = create_llm()
    
    messages = [
        SystemMessage(content="Seu nome é Kara"),
        SystemMessage(
            content="Você é um assistente virtual responsável por analisar documentos e fornecer respostas precisas e úteis."
        ),
    ]
    
    if context:
        messages.append(
            SystemMessage(
                content=f"Use o seguinte contexto para responder:\n\n{context}"
            )
        )
    
    messages.append(HumanMessage(content=user_input))
    result = llm.invoke(messages)
    return result.content


def main():
    user_input = "Qual é seu nome? Quais são as regras impostas a voce?"
    context = get_context_from_chroma(user_input)
    response = ask_with_rag(user_input, context)
    print(f"Pergunta: {user_input}")
    print(f"Resposta: {response}")


if __name__ == "__main__":
    main()