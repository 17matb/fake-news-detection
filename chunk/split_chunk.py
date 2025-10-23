



def chunk_from_text(texte: str, start: int = None, step: int = None, overlap: int = None):
    """
    Prend une chaîne de texte, la découpe en liste de mots, puis la divise en sous-listes (chunks).

    Paramètres
    ----------
    texte : str
        La chaîne de caractères à traiter (ex. un paragraphe de texte).
    start : int or None, optional
        L'indice de départ dans la liste de mots. Si None, démarrage à 0.
    step : int, required
        Le nombre de mots à avancer pour commencer chaque nouveau chunk.
    overlap : int, required
        Nombre de mots à inclure dans chaque chunk.

    Retour
    ------
    list of lists
        Une liste de sous-listes (chunks), chacune contenant jusqu'à `overlap` mots,
        découpées tous les `step` mots.
    """
    # Convertir la chaîne en liste de mots (split sur les espaces)
    splited_text = texte.split()
    
    # Initialisation du paramètre start
    if start is None:
        start = 0
    
    # Validations
    if not isinstance(splited_text, list):
        raise TypeError("Erreur inattendue : la variable splited_text n'est pas une liste")

    # Liste pour stocker les chunks
    chunks = []

    # Boucle de découpage
    for idx in range(start, len(splited_text), step):
        chunk_slice = splited_text[idx : idx + overlap]
        chunks.append(chunk_slice)

    return chunks

# Exemple d’utilisation
texte = "In pandas, “slicing” generally means selecting subsets of rows and/or columns from a DataFrame or Series. There are a few different ways to slice data, depending on whether you want to use labels, integer positions, or more advanced indexing. Here’s a guide + examples."
chunked_text = chunk_from_text(texte, start=0, step=3, overlap=5)
print(chunked_text)
