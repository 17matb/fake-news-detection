from typing import final

import pandas as pd

from data_handler.text_cleaning import text_cleaning


@final
class DataHandler:
    def __init__(self, csv_path: str):
        self.csv_path = csv_path

    def load(self):
        print(f"· LOADING CSV DATA FROM `{self.csv_path}` INTO A DATAFRAME")
        self.df: pd.DataFrame = pd.read_csv(self.csv_path)
        print(f"· DATAFRAME PREVIEW:\n{self.df}")
        return self

    def explore(self):
        print("· EXPLORING DATA")
        if self.df is None:
            raise ValueError("× Dataframe not found")
        exploration_info = {
            "shape": self.df.shape,
            "columns": self.df.columns.tolist(),
            "dtypes": self.df.dtypes.to_dict(),
            "missing": self.df.isna().sum().to_dict(),
        }
        print(f"· SHAPE: {exploration_info['shape']}")
        print(f"· COLUMNS: {exploration_info['columns']}")
        print(f"· DTYPES: {exploration_info['dtypes']}")
        print(f"· MISSING: {exploration_info['missing']}")
        return self

    def clean(self):
        print("· CLEANING DATA")
        self.clean_df: pd.DataFrame = self.df.copy()

        self.clean_df = self.clean_df.drop_duplicates("text")
        print(
            f"· DROPPED {self.df['text'].duplicated().sum()} DUPLICATES FOR `text` COLUMN"
        )

        for column in ["title", "text", "subject"]:
            self.clean_df[column] = self.clean_df[column].apply(text_cleaning)
        print("· DECODED HTML ENTITIES BACK TO THEIR ORIGINAL CHARACTERS")
        print("· REMOVED HTML TAGS")
        print("· REMOVED OTHER UNWANTED FORMATTING TAGS")
        print("· REMOVED URLS")
        print("· NORMALIZED WHITE SPACES")
        print("· REMOVED SPECIAL CARACTERS")

        self.clean_df["date"] = pd.to_datetime(
            self.clean_df["date"], errors="coerce", format="mixed"
        )
        print("· CONVERTED `date` COLUMN TO DATETIME FORMAT")

        self.clean_df = self.clean_df[self.clean_df["title"].str.strip().astype(bool)]  # pyright: ignore[reportAttributeAccessIssue]
        self.clean_df = self.clean_df[self.clean_df["text"].str.strip().astype(bool)]  # pyright: ignore[reportAttributeAccessIssue]
        print("· DELETED ENTRIES WITH EMPTY `title` OR `text` VALUES")

        print(f"· CLEAN DATAFRAME PREVIEW:\n{self.clean_df}")
        return self
