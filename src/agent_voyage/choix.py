"""Etapes 3 et 4b du Grafcet : choisir le voyage, en Python, sans le modele."""

from agent_voyage.voyages import VOYAGES

GOUTS = ["plage", "montagne", "ville", "sport", "detente"]


def choisir_voyage(criteres: dict) -> dict | None:
    """Renvoie le voyage qui convient le mieux, ou None si aucun critere n'est rempli.

    Regle decidee le 21/10 :
    - acces_handicap a True est un besoin : les voyages non accessibles sont exclus ;
    - chaque Oui du client satisfait par le voyage vaut 10 points ;
    - chaque Non du client que le voyage heurte coute 1 point ;
    - a egalite, le premier voyage du fichier passe devant.
    """
    # Etape 3 : au moins un critere rempli ?
    if all(criteres.get(critere) is None for critere in GOUTS + ["acces_handicap"]):
        return None

    candidats = VOYAGES
    if criteres.get("acces_handicap") is True:
        candidats = [voyage for voyage in VOYAGES if voyage["acces_handicap"]]

    def score(voyage: dict) -> int:
        oui = sum(1 for gout in GOUTS if criteres.get(gout) is True and voyage[gout])
        non = sum(1 for gout in GOUTS if criteres.get(gout) is False and voyage[gout])
        return 10 * oui - non

    # Etape 4b : max garde le premier des meilleurs, donc l'ordre du fichier
    return max(candidats, key=score)
