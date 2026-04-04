import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.chroma import (
    get_chroma_client,
    create_collection,
    add_document,
    load_document,
)


def get_all_documents(data_dir=None):
    """Lista todos os arquivos .txt na pasta data/.
    
    Returns:
        Lista de tuplas (doc_id, filepath, content).
    """
    if data_dir is None:
        data_dir = os.path.join(os.path.dirname(__file__), "data")
    
    documents = []
    for filename in os.listdir(data_dir):
        if filename.endswith(".txt"):
            filepath = os.path.join(data_dir, filename)
            doc_id = os.path.splitext(filename)[0]
            content = load_document(filename)
            documents.append((doc_id, filename, content))
    
    return documents


def ingest_all(reset=False):
    """Ingesta todos os documentos da pasta data/ no Chroma.
    
    Args:
        reset: Se True, limpa a coleção antes de ingerir.
    """
    client = get_chroma_client()
    collection = create_collection(client, "documents")
    
    if reset:
        # Limpa a coleção existente
        client.delete_collection("documents")
        collection = client.create_collection("documents")
        print("Coleção limpa e recriada.")
    
    documents = get_all_documents()
    
    if not documents:
        print("Nenhum documento .txt encontrado em data/.")
        return
    
    print(f"Encontrados {len(documents)} documento(s).")
    
    for doc_id, filename, content in documents:
        add_document(collection, content, doc_id, {"source": filename})
        print(f"  ✓ {filename} ({len(content)} caracteres)")
    
    print(f"\nIngestão concluída! Total: {len(documents)} documento(s).")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Ingest documentos no Chroma")
    parser.add_argument(
        "--reset", 
        action="store_true",
        help="Limpa a coleção antes de ingerir"
    )
    
    args = parser.parse_args()
    ingest_all(reset=args.reset)


if __name__ == "__main__":
    main()