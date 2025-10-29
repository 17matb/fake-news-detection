# Système de Détection de Fake News

![python](https://img.shields.io/badge/python-3.12-green)
![ChromaDB](https://img.shields.io/badge/ChromaDB-1.2.1-blue)
![Ollama](https://img.shields.io/badge/Ollama-0.6.0-white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.50-orange)

Un système sophistiqué RAG (Retrieval-Augmented Generation) pour détecter les fake news en comparant des articles à une base de données vérifiée utilisant la similarité sémantique et l'analyse par LLM local.

## Aperçu du Projet

Ce projet implémente un système alimenté par l'IA qui analyse des articles de presse pour déterminer leur véracité en les comparant à une base de données d'articles pré-vérifiés étiquetés "True" ou "Fake". Le système utilise ChromaDB pour le stockage vectoriel et Ollama pour l'inférence LLM locale.

### Fonctionnalités Principales
- **Pipeline de Traitement des Données** : Nettoie, découpe et vectorise les articles de presse
- **Recherche Sémantique** : Trouve des articles similaires utilisant des embeddings vectoriels
- **Analyse LLM** : Utilise des modèles locaux via Ollama pour la classification
- **Interface Double** : Interface en ligne de commande et interface web Streamlit
- **Exécution Locale** : Tous les modèles s'exécutent localement pour la confidentialité et le contrôle

## Architecture du Système

```
fake-news-detection/
├── app/                  # Interface web Streamlit
├── chroma/               # Client ChromaDB et gestion
├── data_handler/         # Utilitaire de chargement et nettoyage des données
├── function_chunk/       # Fonctionnalité de découpage de texte
├── pipelines/            # Pipeline principal de traitement des données
├── prompt/               # Système RAG et construction de prompts
└── tests/                # Suites de tests
```

## Démarrage Rapide

### Prérequis

- Python 3.12+
- [Ollama](https://ollama.ai/) installé et fonctionnel
- Modèles Ollama requis : `all-minilm:latest` et `phi3:3.8b`

### Installation

1. **Installer Ollama et les modèles requis :**
```bash
# Installer Ollama (suivre les instructions sur https://ollama.ai/)
ollama pull all-minilm:latest
ollama pull phi3:3.8b
```

2. **Démarrer le serveur Ollama :**
```bash
ollama serve
```

3. **Configurer l'environnement Python :**
```bash
# Utiliser uv
uv sync
```

### Utilisation

#### Interface Ligne de Commande

```bash
# Exploration des données
uv run main.py -e

# Traitement des données et insertion dans ChromaDB
uv run main.py -i

# Analyser un article de presse
uv run main.py -r
```

#### Interface Web (Streamlit)

```bash
uv run python -m streamlit run app/app.py
```

## Configuration

### Fichiers de Données
Placer vos fichiers de dataset dans le répertoire `data/` :
- `Fake.csv` - Articles étiquetés comme fake news
- `True.csv` - Articles étiquetés comme vraies informations

### Configuration des Modèles
Le système utilise deux modèles Ollama :
- **Modèle d'Embedding** : `all-minilm:latest` pour les embeddings vectoriels
- **Modèle LLM** : `phi3:3.8b` pour la génération de texte et classification

## Comment Ça Marche

### 1. Pipeline de Traitement des Données
- **Chargement** : Lit les fichiers CSV et les combine en un seul DataFrame
- **Exploration** : Analyse la forme des données, les types et les valeurs manquantes
- **Nettoyage** : Supprime les balises HTML, URLs, caractères spéciaux et normalise le texte
- **Découpage** : Divise les articles en morceaux avec chevauchement pour une meilleure récupération

### 2. Stockage Vectoriel
- **Génération d'Embeddings** : Crée des embeddings vectoriels pour chaque morceau de texte
- **Intégration ChromaDB** : Stocke les vecteurs avec métadonnées dans une base de données persistante
- **Normalisation** : Applique la normalisation L2 aux vecteurs pour une meilleure recherche de similarité

### 3. Système RAG
- **Traitement des Requêtes** : Vectorise l'entrée utilisateur et trouve des articles similaires
- **Construction du Contexte** : Construit le contexte du prompt à partir des articles récupérés
- **Classification** : Utilise le LLM pour analyser l'article et fournir un verdict True/Fake avec justification

## Détails Techniques

### Composants Principaux

- **ChromaClient** : Classe singleton gérant les connexions ChromaDB
- **DataHandler** : Gère le chargement, l'exploration et le nettoyage des données
- **Pipeline** : Orchestre le flux de travail complet du traitement des données
- **RAGSystem** : Implémente le pipeline de génération augmentée par récupération
- **PromptBuilder** : Construit les prompts LLM avec contexte pertinent

### Traitement du Texte
- Décodage des entités HTML et suppression des balises
- Suppression des URLs et caractères spéciaux
- Normalisation des espaces et mise en minuscules
- Découpage du texte avec chevauchement configurable

## Tests

Exécuter la suite de tests pour vérifier tous les composants :

```bash
# Exécuter tous les tests
uv run pytest tests/

# Exécuter des modules de test spécifiques
uv run pytest tests/test_data_cleaner.py

uv run pytest tests/test_split_chunk.py

uv run pytest tests/test_prompt_builder.py
```

## Considérations de Performance

- **Taille des Morceaux** : Ajuster les paramètres `step` et `overlap` dans `chroma_manager.py` pour une récupération optimale
- **Traitement par Lots** : Les grands datasets sont traités par lots de taille configurable
- **Normalisation Vectorielle** : Améliore la précision de la recherche de similarité
- **Sélection des Modèles** : Équilibre entre précision et vitesse d'inférence

## Évaluation

Le système peut être évalué sur :
- **Précision de Classification** : Comparaison des verdicts LLM avec les labels réels
- **Qualité de Récupération** : Précision et rappel de la récupération d'articles similaires
- **Cohérence des Réponses** : Qualité des justifications fournies par le LLM

## Contribution

1. Forker le repository
2. Créer une branche de fonctionnalité
3. Ajouter des tests pour les nouvelles fonctionnalités
4. S'assurer que tous les tests passent
5. Soumettre une pull request

## Licence
Ce projet n'est pas sous licence open-source.  
Il a été développé dans le cadre d’un projet d'étude et est destiné à un usage éducatif uniquement.  
Toute réutilisation ou diffusion du code nécessite l’accord préalable de l’auteur.

## Auteurs
**Équipe de développement**
- Matthis - Nabil - Loïc : Développement principal

**Supervision**

- Nadège - Maxime

## Dépannage

### Problèmes Courants

1. **Erreurs de Connexion Ollama**
   - Vérifier que `ollama serve` est en cours d'exécution
   - Vérifier que les modèles sont téléchargés avec `ollama list`

2. **Persistance ChromaDB**
   - Vérifier les permissions d'écriture dans `./chroma_db/`
   - Vider le répertoire de la base de données en cas de problèmes de migration

3. **Problèmes de Mémoire**
   - Réduire la taille des lots dans `ChromaManager.add_dataframe_to_collection()`
   - Utiliser des modèles d'embedding plus petits si nécessaire

### Obtenir de l'Aide

- Consulter les fichiers de test pour des exemples d'utilisation
- Revoir la documentation ChromaDB pour les opérations de base de données vectorielles
- Consulter la documentation Ollama pour la gestion des modèles

---

*Construit à des fins éducatives en développement IA et applications NLP.*
