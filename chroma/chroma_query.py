def query_collection(
    collection, query_texts, n_results, include=["documents", "metadatas", "distances"]
):
    """
    Interroge une collection ChromaDB avec un ou plusieurs textes.

    Args:
        collection: instance de collection ChromaDB
        query_texts: str ou list de str
        n_results: nombre de résultats à récupérer
        include: liste des champs à inclure dans la réponse

    Returns:
        dict contenant 'documents', 'metadatas', 'distances', etc.
    """
    if isinstance(query_texts, str):
        query_texts = [query_texts]

    return collection.query(
        query_texts=query_texts, n_results=n_results, include=include
    )
