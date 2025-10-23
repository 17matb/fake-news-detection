import pandas as pd
import pytest


def create_mock_dataset():
    data = {
        "title": ["Title 1", "Title 2", "Title 3"],
        "text": [
            "Fake News : Aliens landind on Earth !",
            "Donald Trump is a first super genius !",
            "Alibaba and the 40 thiefs !",
        ],
        "label": ["False", "False", "True"],
    }

    df = pd.DataFrame(data)
    return df


def test_mock_dataset_structure():
    df = create_mock_dataset()

    # Vérifie si c'est un DF
    assert isinstance(df, pd.DataFrame)
    # Vérifie les colonnes
    assert set(df.columns) == {"title", "text", "label"}
    # Vérifie le nombre de lignes
    assert len(df) == 3


def text_mock_dataset_content_not_null():
    df = create_mock_dataset()
    # Vérifie que toutes les colonnes existent
    for col in ["title", "text", "label"]:
        assert col in df.columns
    # Vérifie que les labels sont valides
    assert all(l in ["True", "Fake"] for l in df["label"] if l != "")


def text_cleaning_on_mock_data():
    df = create_mock_dataset()
    # from import # A mettre à jour quand module prêt
    df["clean_text"] = df["text"].apply()  # Appliquer le module
    assert all("<" not in c and "http" not in c for c in df["clean_text"])


def test_pipeline_on_mock_dataset():
    df = create_mock_dataset()
    # from import # A mettre à jour quand module prêt

    # Prétraitement
    df["clean_text"] = df["text"].apply(clean_text)  # clean_text à adapter selon module
    df["clean_text"] = df["clean_text"].apply(
        to_lower
    )  # to_lower à adapter selon module

    # Chunk
    df["chunk"] = df["clean_text"].apply(
        lambda x: chunk_text(x, chunk_size=5)
    )  # chunk_test à adapté selon module

    # Embedding
    df["embedding"] = df["clean_text"].apply(
        lambda chunks: [embedding(c) for c in chunks]
    )  # embedding à adapter selon module

    # Vérification
    for idx, row in df.iterrows():
        # Chunks = liste
        assert isinstance(row["chunks"], list)

        # Embedding = liste de vecteurs
        for vec in row["embedding"]:
            assert isinstance(vec, list)
