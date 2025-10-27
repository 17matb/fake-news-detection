import re
from html import unescape


def text_cleaning(text):
    # unescape text
    text = unescape(text)
    # remove html tags
    text = re.sub(r"<.*?>", "", text)
    # remove urls
    text = re.sub(r"http\S+|www\S+", "", text)
    # remove special characters
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)
    # normalize spaces
    text = re.sub(r"\s+", " ", text).strip()
    # set to lowercase
    text = text.lower()
    return text
