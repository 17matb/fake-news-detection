# fichier : test_prompt_builder.py

import unittest
from unittest.mock import patch, MagicMock
from prompt.prompt_builder import PromptBuilder  # adapte selon ton chemin

class TestPromptBuilder(unittest.TestCase):

    def setUp(self):
        self.article_text = "Donald Trump shares a controversial photo on social media."
        self.model_embedding = "mxbai-embed-large"
        self.model_llm = "llama3"
        self.builder = PromptBuilder(self.article_text, self.model_embedding, self.model_llm)

    @patch("ollama.embed")
    def test_generate_embedding(self, mock_embed):
        # Mock de la réponse de ollama.embed
        mock_embed.return_value = {"embeddings": [0.1, 0.2, 0.3]}
        emb = self.builder.generate_embedding()
        self.assertEqual(emb, [0.1, 0.2, 0.3])
        mock_embed.assert_called_once_with(model=self.model_embedding, input=self.article_text)

    def test_build_context_for_prompt(self):
        # Fake search_results
        search_results = {
            "documents": [["Doc 1 text", "Doc 2 text"]],
            "metadatas": [[
                {"subject": "Politics", "date": "2025-10-27", "label": "True"},
                {"subject": "Media", "date": "2025-10-26", "label": "Fake"}
            ]]
        }
        context = self.builder.build_context_for_prompt(search_results)
        self.assertIn("Doc 1 text", context)
        self.assertIn("Politics", context)
        self.assertIn("Fake", context)

    def test_build_prompt(self):
        context = "Some context text"
        prompt = self.builder.build_prompt(context)
        self.assertIn("Some context text", prompt)
        self.assertIn(self.article_text, prompt)
        self.assertIn("Label", prompt)

    @patch("ollama.generate")
    def test_predict_label(self, mock_generate):
        prompt = "Test prompt"
        mock_generate.return_value = {"response": "Label: True\nJustification: Example."}
        response = self.builder.predict_label(prompt)
        self.assertEqual(response, "Label: True\nJustification: Example.")
        mock_generate.assert_called_once_with(model=self.model_llm, prompt=prompt)

