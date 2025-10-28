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
        # Génére l'embedding du texte à vérifier
        emb_response = ollama.embed(
            model=self.model_embedding,
            input=self.article_text
        )
        self.data = emb_response["embeddings"]

        return self.data 
    
    def build_context_for_prompt(self, search_results):
        # Rechercher les articles les plus similaires dans la base vectorielle
        # Prend le retour de la fonction query_collection qui a était vectorisé au préalable
        
        search_results = self.collection.query(
            query_embeddings=self.data,
            n_results=3,
            include=["documents", "metadatas", "distances"]
        )

        # Récupérer les documents les plus proches
        similar_docs = search_results["documents"][0]
        similar_meta = search_results["metadatas"][0]

        # Construire le contexte à donner au LLM
        context = "\n\n".join([
            f"- Sujet : {meta['subject']}\n  Date : {meta['date']}\n  Label : {meta['label']}\n  Texte : {doc['text']}..."
            for doc, meta in zip(similar_docs, similar_meta)
        ])
        return context
    
    def build_prompt(self, context):
        # Construire le prompt complet pour le LLM
        prompt = f"""
                You are an expert in detecting fake news. 
                You have a knowledge base containing articles that have already been verified, with their metadata:
                - subject: main topic
                - date: publication date
                - label: “True” or “Fake”
                - text: content of the article.

                Here are some similar articles from your database:
                {context}

                Your task is to analyze the following new article and determine whether it is “True” or “Fake.”

                New article to analyze:
        ---
        {self.article_text}
        ---

        Respond only with:
        Label: "True" or "Fake"
        Justification: in 2 sentences maximum, based on the similarities or tone of the article.
        """
        return prompt
    
    def predict_label(self, prompt):
        # Appele le modèle de langage pour obtenir la classification
        response = ollama.generate(
            model=self.model_llm,
            prompt=prompt
        )

        # Retourne la réponse
        return response["response"]