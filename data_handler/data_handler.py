from html import unescape
from typing import final

import pandas as pd

from data_handler.cleaning_utils import CleaningUtils


@final
class DataHandler:
    def __init__(self, csv_path: str):
        self.csv_path = csv_path

    def load(self):
        print(f"-> LOADING CSV DATA FROM `{self.csv_path}` INTO A DATAFRAME")
        self.df: pd.DataFrame = pd.read_csv(self.csv_path)
        print(f"· DATAFRAME PREVIEW:\n{self.df}")
        return self

    def explore(self):
        print("\n-> EXPLORING DATA")
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
        print("\n-> CLEANING DATA")
        self.clean_df: pd.DataFrame = self.df.copy()

        self.clean_df["title"] = self.clean_df["title"].astype(str)
        self.clean_df["text"] = self.clean_df["text"].astype(str)
        print("· CONVERTED `title` AND `text` COLUMNS TO STRING TYPE")

        self.clean_df = self.clean_df.drop_duplicates("text")
        print(
            f"· DROPPED {self.df['text'].duplicated().sum()} DUPLICATES FOR `text` COLUMN"
        )

        self.clean_df["title"] = self.clean_df["title"].apply(lambda x: unescape(x))
        self.clean_df["text"] = self.clean_df["text"].apply(lambda x: unescape(x))
        print("· DECODED HTML ENTITIES BACK TO THEIR ORIGINAL CHARACTERS")

        self.clean_df["title"] = self.clean_df["title"].apply(
            CleaningUtils.remove_html_tags
        )
        self.clean_df["text"] = self.clean_df["text"].apply(
            CleaningUtils.remove_html_tags
        )
        print("· REMOVED HTML TAGS IN `title` AND `text` COLUMNS")

        self.clean_df["title"] = self.clean_df["title"].apply(
            CleaningUtils.remove_starts_ends_brackets
        )
        self.clean_df["text"] = self.clean_df["text"].apply(
            CleaningUtils.remove_starts_ends_brackets
        )
        print("· REMOVED OTHER UNWANTED FORMATTING TAGS IN `title` AND `text` COLUMNS")

        self.clean_df["title"] = self.clean_df["title"].apply(CleaningUtils.remove_urls)
        self.clean_df["text"] = self.clean_df["text"].apply(CleaningUtils.remove_urls)
        print("· REMOVED URLS IN `title` AND `text` COLUMNS")

        self.clean_df["title"] = self.clean_df["title"].apply(
            CleaningUtils.normalize_spaces
        )
        self.clean_df["text"] = self.clean_df["text"].apply(
            CleaningUtils.normalize_spaces
        )
        print("· NORMALIZED WHITE SPACES IN `title` AND `text` COLUMNS")

        self.clean_df["title"] = self.clean_df["title"].apply(
            CleaningUtils.remove_special_characters
        )
        self.clean_df["text"] = self.clean_df["text"].apply(
            CleaningUtils.remove_special_characters
        )
        print("· REMOVED SPECIAL CHARACTERS IN `title` AND `text` COLUMNS")

        self.clean_df["date"] = pd.to_datetime(
            self.clean_df["date"], errors="coerce", format="mixed"
        )
        print("· CONVERTED `date` COLUMN TO DATETIME FORMAT")

        self.clean_df["title"] = self.clean_df["title"].str.lower()
        self.clean_df["text"] = self.clean_df["text"].str.lower()
        self.clean_df["subject"] = self.clean_df["subject"].str.lower()
        print("· SET EVERY STRING TO LOWERCASE")

        self.clean_df = self.clean_df[self.clean_df["title"].str.strip().astype(bool)]
        self.clean_df = self.clean_df[self.clean_df["text"].str.strip().astype(bool)]
        print("· DELETED ENTRIES WITH EMPTY `title` OR `text` VALUES")

        print(f"· CLEAN DATAFRAME PREVIEW:\n{self.clean_df}")
        return self
