import pytest
import chromadb


def test_chroma_connection(tmp_path):
    client = chromadb.PersistentClient(path=tmp_path)

    collections = client.create_collection(name="collection_test")

    collections.add(
        ids=["ids"],
        embeddings=[0.1, 0.3, 0.6],
        metadatas=[{"label": "True", "subject": "Test"}],
        documents=["Test ChromaDB"],
    )

    results = collections.query(query_embeddings=[[0.1, 0.3, 0.6]], n_results=1)

    assert len(results["ids"][0]) == 1
    assert results["ids"][0][0] == "ids"
    assert results["metadatas"][0][0]["subject"] == "Test"
    assert "Test ChromaDB" in results["documents"][0][0]
