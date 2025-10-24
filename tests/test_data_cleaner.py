from unittest.mock import patch

import pandas as pd
from data_handler.data_handler import DataHandler


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
    assert all(label in ["True", "Fake"] for label in df["label"] if label != "")


def text_cleaning_on_mock_data():
    df = create_mock_dataset()

    with patch("pandas.read_csv", return_value=df):
        handler = DataHandler(csv_path="test.csv")
        handler.load().clean()

    assert all("<" not in c and "http" not in c for c in handler.clean_df["text"])
