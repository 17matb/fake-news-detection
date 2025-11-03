import os
import time

import chromadb
from chromadb.utils import embedding_functions

from chroma.singleton import SingletonMeta


class ChromaClient(metaclass=SingletonMeta):
    """
    Singleton qui gère la connexion à ChromaDB et l'embedding Ollama.
    """

    def __init__(
        self, db_path: str = "./chroma_db/", model_name: str = "all-minilm:latest"
    ):
        self.client = chromadb.PersistentClient(path=db_path)
        self.model_name = model_name
        self.embedding_function = None

    def get_client(self):
        """
        Retourne le client Chroma
        """
        return self.client

    def get_embedding_function(self):
        """
        Retourne la fonction d'embedding
        """
        if self.embedding_function is None:
            max_retries = 5
            retry_delay = 2

            for attempt in range(max_retries):
                try:
                    self.embedding_function = (
                        embedding_functions.OllamaEmbeddingFunction(
                            model_name=self.model_name,
                            url=os.getenv("OLLAMA_HOST", "http://ollama:11434"),
                        )
                    )
                    embed_test = self.embedding_function(["test"])
                    print(f"connexion à Ollama réussie -> {embed_test}")
                    break
                except Exception as e:
                    if attempt < max_retries - 1:
                        print(
                            f"tentative {attempt + 1}/{max_retries} échouée, nouvelle tentative dans {retry_delay}s..."
                        )
                        time.sleep(retry_delay)
                    else:
                        raise Exception(
                            f"impossible de se connecter à Ollama après {max_retries} tentatives: {e}"
                        )

        return self.embedding_function

    def get_or_create_collection(self, name: str):
        """
        Récupère ou crée une collection persistente avec embeddings.
        """
        return self.client.get_or_create_collection(
            name=name,
            embedding_function=self.embedding_function,
        )
