import re
from html import unescape


class CleaningUtils:
    @staticmethod
    def unescape_text(text):
        return unescape(text)

    @staticmethod
    def remove_html_tags(text):
        return re.sub(r"<.*?>", "", text)

    @staticmethod
    def remove_starts_ends_brackets(text):
        if text.strip().startswith("[") and text.strip().endswith("]"):
            return ""
        return text

    @staticmethod
    def remove_urls(text):
        return re.sub(r"http\S+|www\S+", "", text)

    @staticmethod
    def normalize_spaces(text):
        return re.sub(r"\s+", " ", text).strip()

    @staticmethod
    def remove_special_characters(text):
        return re.sub(r"[^a-zA-Z0-9\s]", "", text)
