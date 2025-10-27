from typing import final

import pandas as pd

from data_handler.cleaning_utils import CleaningUtils


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

        for column in ["title", "text"]:
            self.clean_df[column] = (
                self.clean_df[column]
                .apply(CleaningUtils.unescape_text)
                .apply(CleaningUtils.remove_html_tags)
                .apply(CleaningUtils.remove_starts_ends_brackets)
                .apply(CleaningUtils.remove_urls)
                .apply(CleaningUtils.normalize_spaces)
                .apply(CleaningUtils.remove_special_characters)
            )
        print("· DECODED HTML ENTITIES BACK TO THEIR ORIGINAL CHARACTERS")
        print("· REMOVED HTML TAGS IN `title` AND `text` COLUMNS")
        print("· REMOVED OTHER UNWANTED FORMATTING TAGS IN `title` AND `text` COLUMNS")
        print("· REMOVED URLS IN `title` AND `text` COLUMNS")
        print("· NORMALIZED WHITE SPACES IN `title` AND `text` COLUMNS")
        print("· REMOVED SPECIAL CARACTERS IN `title` AND `text` COLUMNS")

        self.clean_df["date"] = pd.to_datetime(
            self.clean_df["date"], errors="coerce", format="mixed"
        )
        print("· CONVERTED `date` COLUMN TO DATETIME FORMAT")

        self.clean_df["title"] = self.clean_df["title"].str.lower()
        self.clean_df["text"] = self.clean_df["text"].str.lower()
        self.clean_df["subject"] = self.clean_df["subject"].str.lower()
        print("· SET EVERY STRING TO LOWERCASE")

        self.clean_df = self.clean_df[self.clean_df["title"].str.strip().astype(bool)]  # pyright: ignore[reportAttributeAccessIssue]
        self.clean_df = self.clean_df[self.clean_df["text"].str.strip().astype(bool)]  # pyright: ignore[reportAttributeAccessIssue]
        print("· DELETED ENTRIES WITH EMPTY `title` OR `text` VALUES")

        print(f"· CLEAN DATAFRAME PREVIEW:\n{self.clean_df}")
        return self
