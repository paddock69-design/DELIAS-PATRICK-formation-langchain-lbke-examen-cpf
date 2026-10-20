"""Les voyages de l'agence.

Le fichier voyages.json est garde tel que le sujet le donne (syntaxe corrigee
seulement). Ce module le traduit dans le vocabulaire des 6 criteres.
"""

import json
from pathlib import Path

FICHIER_VOYAGES = Path(__file__).parent / "voyages.json"

# Les labels du JSON qui ne s'ecrivent pas comme le critere correspondant
CORRESPONDANCE_LABELS = {"détente": "detente"}


def traduire(voyage_brut: dict) -> dict:
    """Traduit un voyage du JSON du sujet en 6 criteres vrai/faux."""
    labels = [CORRESPONDANCE_LABELS.get(label, label) for label in voyage_brut["labels"]]
    return {
        "nom": voyage_brut["nom"],
        "plage": "plage" in labels,
        "montagne": "montagne" in labels,
        "ville": "ville" in labels,
        "sport": "sport" in labels,
        "detente": "detente" in labels,
        "acces_handicap": voyage_brut["accessibleHandicap"] == "oui",
    }


def charger_voyages() -> list[dict]:
    """Lit voyages.json et renvoie les voyages traduits."""
    with open(FICHIER_VOYAGES, encoding="utf-8") as fichier:
        return [traduire(voyage) for voyage in json.load(fichier)]


VOYAGES = charger_voyages()
