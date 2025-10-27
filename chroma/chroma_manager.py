import pandas as pd
from chromadb import Collection
from function_chunk.split_chunk import chunk_text
from chroma_client import ChromaClient
from chroma_query import query_collection


class ChromaManager:
    def __init__(self, collection_name):
        self.client = ChromaClient()
        self.embed_function = self.client.embedding_function()
        self.collection = self.client.get_or_create_collection(
            name=collection_name, embedding_function=self.embed_function
        )

    def add_dataframe_to_collection(
        self,
        df: pd.Dataframe,
        prefix: str,
        step: int = 50,
        overlap: int = 10,
        batch_size: int = 20,
    ):
        """
        Ajoute un DataFrame complet dans la collection Chroma avec chunks + embeddings.
        """

        ids, documents, metadatas, embeddings = [], [], [], []
        for idx, row in df.iterrows():
            chunks = chunk_text(row["text"], step=step, overlap=overlap)

            for i, chunk in enumerate(chunks):
                ids.append(f"{prefix}_{idx}_{i}")
                documents.append(chunk)
                metadatas.append(
                    {
                        "title": row.get("title"),
                        "subject": row.get("subject"),
                        "date": str(row.get("date")),
                        "label": row.get("label"),
                        "chunk_index": i,
                    }
                )

                # Embedding du chunk
                embeddings.append(self.embed_function([chunk])[0])

                if len(documents) >= batch_size:
                    self.collection.add(
                        ids=ids,
                        documents=documents,
                        metadatas=metadatas,
                        embeddings=embeddings,
                    )
                ids, documents, metadatas, embeddings = [], [], [], []

        # Dernier batch
        if len(documents) > 0:
            self.collection.add(
                ids=ids, documents=documents, metadatas=metadatas, embeddings=embeddings
            )

    def query(self, text, n_results):
        return query_collection(self.collection, text, n_results)
