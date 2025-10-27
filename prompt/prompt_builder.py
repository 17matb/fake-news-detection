import ollama

class PromptBuilder():

    """
        Prend un texte d'article et retourne une prédiction True/Fake
        en utilisant RAG (Recherche + LLM via Ollama).
    """

    def __init__(self, article_text, model_embedding, model_llm):
        self.article_text = article_text
        self.model_embedding = model_embedding
        self.model_llm = model_llm
        self.data = None

    def generate_embedding(self):
        # Générer l'embedding du texte à vérifier
        emb_response = ollama.embed(
            model=self.model_embedding,
            input=self.article_text
        )
        embedding = emb_response["embeddings"]

        return embedding 
    
    def retrieve_similar_articles(self):
        # Rechercher les articles les plus similaires dans la base vectorielle
        search_results = collection.query(
            query_embeddings=embedding,
            n_results=3,
            include=["documents", "metadatas", "distances"]
        )

        # Récupérer les documents les plus proches
        similar_docs = search_results["documents"][0]
        similar_meta = search_results["metadatas"][0]

        # Construire le contexte à donner au LLM
        context = "\n\n".join([
            f"- Sujet : {meta['subject']}\n  Date : {meta['date']}\n  Label : {meta['label']}\n  Texte : {doc[:500]}..."
            for doc, meta in zip(similar_docs, similar_meta)
        ])

        # Construire le prompt complet pour le LLM
        prompt = f"""
        Tu es un expert en détection de fake news. 
        Tu disposes d'une base de connaissances contenant des articles déjà vérifiés, avec leurs métadonnées :
        - subject : sujet principal
        - date : date de publication
        - label : "True" ou "Fake"
        - texte : contenu de l’article.

        Voici quelques articles similaires issus de ta base :
        {context}

        Ta tâche est d'analyser le nouvel article suivant et de déterminer s'il est "True" ou "Fake".

        Nouvel article à analyser :
        ---
        {article_text}
        ---

        Réponds uniquement avec :
        Label : "True" ou "Fake"
        Justification : en 2 phrases maximum, basée sur les similarités ou le ton de l’article.
        """

        # Appeler le modèle de langage pour obtenir la classification
        response = ollama.generate(
            model="llama3",
            prompt=prompt
        )

        # Retourner la réponse
        return response["response"]