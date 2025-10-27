from data_handler.data_handler import DataHandler


class Pipeline:
    def __init__(self):
        self.handlers = {
            "fake_news_csv": DataHandler("./data/Fake.csv"),
            "true_news_csv": DataHandler("./data/True.csv"),
        }
        self._is_loaded = False
        self._is_clean = False

    def data_loading(self):
        """
        Loops in handlers dict to call their `load()` method.

        Parameters:
            self

        Returns:
            self
        """
        for name, handler in self.handlers.items():
            print(f"\n-> DATA LOADING FOR `{name}` STARTING...")
            handler.load()
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
        for name, handler in self.handlers.items():
            print(f"\n-> DATA EXPLORATION FOR `{name}` STARTING...")
            handler.explore()
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
        for name, handler in self.handlers.items():
            print(f"\n-> DATA CLEANING FOR `{name}` STARTING...")
            handler.clean()
        self._is_clean = True
        return self
