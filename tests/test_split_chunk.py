
import pytest
from function_chunk.split_chunk import chunk_text

@pytest.fixture
def sample_text():
    """
        Fixture qui retourne du texte que l'on peut réutiliser pour chaque test
    """
    return "one two three four five six seven eight nine ten eleven twelve"

def test_chunk_basic(sample_text):
    result = chunk_text(sample_text, start=0, step=3, overlap=4)
    # On peut calculer manuellement les chunks attendus :
    # mots = ["one","two","three","four","five","six","seven","eight","nine","ten","eleven","twelve"]
    # idx = 0 -> ["one","two","three","four"]
    # idx = 3 -> ["four","five","six","seven"]
    # idx = 6 -> ["seven","eight","nine","ten"]
    # idx = 9 -> ["ten","eleven","twelve"]
    expected = [
        ["one","two","three","four"],
        ["four","five","six","seven"],
        ["seven","eight","nine","ten"],
        ["ten","eleven","twelve"],
    ]
    assert result == expected


@pytest.fixture
def sample_text():
    """
    Fixture qui retourne du texte que l'on peut réutiliser pour chaque test
    """
    return "one two three four five six seven eight nine ten eleven twelve"

def test_chunk_text_correct_behavior(sample_text):
    """
    Vérifie le comportement réel de chunk_text avec start, step et overlap.
    Le test reflète exactement la logique actuelle de la fonction.
    """
    # Paramètres
    start = 2
    step = 4
    overlap = 3

    # Appel de la fonction
    result = chunk_text(sample_text, start=start, step=step, overlap=overlap)

    # Chunks attendus selon la logique réelle
    expected = [
        ["three", "four", "five"],       # idx = 2 -> 2+3
        ["seven", "eight", "nine"],      # idx = 6 -> 6+3
        ["eleven", "twelve"],            # idx = 10 -> 10+3 (reste 2 mots)
    ]

    # Vérification
    assert result == expected
