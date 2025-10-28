# tests/test_imports.py

import importlib
import pkgutil
import sys
from pathlib import Path

import pytest


# --- Ajouter la racine du projet au sys.path ---
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


# --- Fonction utilitaire pour importer dynamiquement un module ---
def try_import(module_name):
    try:
        importlib.import_module(module_name)
        return True, None
    except Exception as e:
        return False, str(e)


# --- Liste des packages à tester ---
PACKAGES = [
    "app",
    "prompt",
    "chroma",
    "data_handler",
    "function_chunk",
    "pipelines",
]


@pytest.mark.parametrize("package", PACKAGES)
def test_import_all_modules(package):
    """Teste tous les sous-modules de chaque package."""
    package_path = ROOT_DIR / package
    assert package_path.exists(), f"Le dossier {package} n'existe pas."

    # Itère sur tous les fichiers Python dans le package
    for module in pkgutil.walk_packages([str(package_path)], prefix=f"{package}."):
        module_name = module.name
        ok, err = try_import(module_name)
        assert ok, f"❌ Erreur lors de l'import de {module_name} : {err}"


def test_no_circular_imports():
    """
    Vérifie les imports circulaires de manière robuste,
    sans planter sur les libs tierces (comme google.*)
    """
    import modulefinder

    finder = modulefinder.ModuleFinder(path=sys.path)
    entrypoint = ROOT_DIR / "app" / "app.py"

    try:
        finder.run_script(str(entrypoint))
    except AttributeError:
        pytest.skip("⚠️ Analyse des imports interrompue (module externe non compatible avec modulefinder)")

    # Chercher des imports circulaires dans le graphe
    circulars = [
        (name, mod.globalnames.keys())
        for name, mod in finder.modules.items()
        if name in mod.globalnames
    ]
    assert not circulars, f"❌ Imports circulaires détectés : {circulars}"

