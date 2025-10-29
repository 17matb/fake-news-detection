from .prompt_builder import PromptBuilder
from chroma.chroma_manager import ChromaManager
import pandas as pd
import re
from collections import Counter

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
    
    def evaluation_rag(self, search_results, response):
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
            predicted_label = match.group(1) # group(1) renvoie juste la partie du groupe capturant ("True").
        else:
            predicted_label = None

        # Labels réels des chunks récupérés
        true_labels = df_chunks["label"].tolist()


        # Prend la majorité des labels 
        # Counter est une classe du module standard Python collections
        majority_label = Counter(true_labels).most_common(1)[0][0] # Counter sert à compter les occurrences de chaque élément dans une liste.
                                                                   # most_common extrait le premier élément du tuple,
        
        
        # Comparaison du label prédit avec les labels des chunks
        matches = sum(1 for label in true_labels if label.lower() == predicted_label.lower())
        percentage = (matches / len(true_labels)) * 100

        # -------------------- A supprimer apres test fonction --------------------------

        # accuracy = int(predicted_label.lower() == majority_label.lower())

        # print(f"Predicted label: {predicted_label}")
        # print(f"Labels des chunks: {true_labels}")
        # print(f"Correspondances: {matches}/{len(true_labels)} ({percentage:.2f}%)")
    
        # # Affichage des comparaisons
        # print(f"Predicted label: {predicted_label}")
        # print(f"Majority label of retrieved chunks: {majority_label}")
        # print(f"Test passed? {accuracy == 1}")

        return percentage