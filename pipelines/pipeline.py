import pandas as pd
from chroma.chroma_manager import ChromaManager
from data_handler.data_handler import DataHandler
from data_handler.text_cleaning import text_cleaning


class Pipeline:
    def __init__(self):
        self.handlers = {
            "fake_news_csv": DataHandler("./data/Fake.csv"),
            "true_news_csv": DataHandler("./data/True.csv"),
        }
        self._is_loaded = False
        self._is_clean = False
        self._is_user_input = False

    def data_loading(self):
        """
        Loops in handlers dict to call their `load()` method.

        Parameters:
            self

        Returns:
            self
        """
        fake_df = self.handlers["fake_news_csv"].load().df
        true_df = self.handlers["true_news_csv"].load().df
        fake_df["label"] = "fake"
        true_df["label"] = "true"

        self.df = pd.concat(
            [
                fake_df,
                true_df,
            ],
            ignore_index=True,
        )
        self._is_loaded = True
        return self

    def data_exploration(self):
        """
        Loops in handlers dict to call their `explore()` method.

        Parameters:
            self

        Returns:
            self
        """
        if not self._is_loaded:
            print("× DATA NEEDS TO BE LOADED, LOADING DATA...")
            self.data_loading()
        print("\n-> DATA EXPLORATION STARTING...")
        self.df = DataHandler.explore(self.df)
        return self

    def data_cleaning(self):
        """
        Loops in handlers dict to call their `clean()` method.

        Parameters:
            self

        Returns:
            self
        """
        if not self._is_loaded:
            print("× DATA NEEDS TO BE LOADED, LOADING DATA...")
            self.data_loading()
        print("\n-> DATA CLEANING STARTING...")
        self.df = DataHandler.clean(self.df)
        self._is_clean = True
        return self

    def chroma_insertion(self):
        """
        Creates chunks, embeds and normalizes them, then inserts into chromaDB

        Parameters:
            self

        Returns:
            self
        """
        if not self._is_clean:
            print("× DATA NEEDS TO BE CLEAN, CLEANING DATA...")
            self.data_cleaning()
        chroma = ChromaManager("news")
        print("\n-> PROCESSING DATA AND INSERTING IT INTO CHROMADB")
        chroma.add_dataframe_to_collection(self.df, "news")

    def process_user_input(self):
        user_input: str = input("Please provide the body of a news article: ")
        print(user_input)
        clean_user_input = text_cleaning(user_input)
        print(clean_user_input)
