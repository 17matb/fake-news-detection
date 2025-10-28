from .prompt_builder import PromptBuilder
from chroma.chroma_manager import ChromaManager
import pandas as pd
import re
from collections import Counter
from sklearn.metrics import accuracy_score

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
    
    def eavaluation_rag(self, search_results, response):
        # search_results est le retour de self.chroma_manager.query(article_text, n_results=3) / def analyse_aticle
        retrieved_chunks = []

        for doc, meta, dist in zip(
            search_results['documents'][0],
            search_results['metadatas'][0],
            search_results['distances'][0]
        ):
            retrieved_chunks.append({
                "text": doc,
                "subject": meta['subject'],
                "date": meta['date'],
                "label": meta['label'],   # vrai label
                "distance": dist
            })

        # Convertir en DataFrame pour plus de clarté
        df_chunks = pd.DataFrame(retrieved_chunks)
        pass
                
        # Réponse du LLM
        llm_text = response["response"]

        # Extraire le Label entre les ```plaintext``` ou après "Label :"
        match = re.search(r"Label\s*:\s*(True|Fake)", llm_text, re.IGNORECASE)
        if match:
            predicted_label = match.group(1)
        else:
            predicted_label = None

        # Labels réels des chunks récupérés
        true_labels = df_chunks["label"].tolist()


        # Prend la majorité des labels 
        majority_label = Counter(true_labels).most_common(1)[0][0]

        # Comparaison
        accuracy = int(predicted_label.lower() == majority_label.lower())
        print(f"Predicted label: {predicted_label}")
        print(f"Majority label of retrieved chunks: {majority_label}")
        print(f"Test passed? {accuracy == 1}")