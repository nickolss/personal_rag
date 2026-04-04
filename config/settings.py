
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()


def get_groq_api_key() -> str:
    """Retorna a API key do Groq das variáveis de ambiente."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError(
            "GROQ_API_KEY não encontrada. "
            "Configure-a no arquivo .env ou como variável de ambiente."
        )
    return api_key