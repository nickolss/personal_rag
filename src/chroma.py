import os
import chromadb
from chromadb.config import Settings

CHROMA_PERSIST_DIR = os.path.join(os.path.dirname(__file__), "..", "chroma_db")


def get_chroma_client(persist=True):
    # Cria e retorna um cliente Chroma.    
    if persist:
        os.makedirs(CHROMA_PERSIST_DIR, exist_ok=True)
        return chromadb.PersistentClient(path=CHROMA_PERSIST_DIR)
    return chromadb.Client()


def load_document(filepath):
    data_dir = os.path.join(os.path.dirname(__file__), "data")
    full_path = os.path.join(data_dir, filepath)
    with open(full_path, "r", encoding="utf-8") as f:
        return f.read()


def create_collection(client, name="rules"):
    try:
        collection = client.create_collection(name=name)
    except Exception:
        collection = client.get_collection(name=name)
    return collection


def add_document(collection, text, doc_id, metadata=None):
    collection.add(
        documents=[text],
        ids=[doc_id],
        metadatas=[metadata] if metadata else None,
    )


def query_collection(collection, query_text, n_results=2):
    return collection.query(
        query_texts=[query_text],
        n_results=n_results,
    )