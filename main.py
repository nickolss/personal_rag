from src.rag import create_llm, create_system_prompt, ask_llm


def main():
    llm = create_llm()
    
    messages = create_system_prompt()
    
    user_input = "Olá, qual é o seu nome e qual é a sua função?"
    result = ask_llm(llm, messages, user_input)
    
    print(result.content)


if __name__ == "__main__":
    main()