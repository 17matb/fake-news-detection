from chroma.chroma_manager import ChromaManager

from .prompt_builder import PromptBuilder


class RAGSystem:
    def __init__(self, collection_name="news", model_lm="phi3:3.8b"):
        self.chroma_manager = ChromaManager(collection_name)
        self.embedding_functions = self.chroma_manager.embed_function

        self.model_embedding = "all-minilm:latest"
        self.model_llm = model_lm

    def analyze_article(self, article_text):
        try:
            # Recherche des articles similaires
            search_results = self.chroma_manager.query(article_text, n_results=3)

            # Construction du prompt
            prompt_builder = PromptBuilder(
                article_text=article_text,
                model_embedding=self.model_embedding,
                model_llm=self.model_llm,
            )

            # Construction du contexte
            context = prompt_builder.build_context_for_prompt(search_results)

            # Construction du prompt final
            prompt = prompt_builder.build_prompt(context)

            # Prédiction
            response = prompt_builder.predict_label(prompt)

            return response

        except Exception as e:
            return f"Erreur lors de l'analyse: {e}"
