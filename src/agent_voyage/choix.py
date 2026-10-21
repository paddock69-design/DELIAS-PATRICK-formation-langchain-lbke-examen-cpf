"""Etapes 3 et 4b du Grafcet : choisir le voyage, en Python, sans le modele."""

from agent_voyage.voyages import VOYAGES

GOUTS = ["plage", "montagne", "ville", "sport", "detente"]


def aucun_critere(criteres: dict) -> bool:
    """Etape 3 : vrai si le client n'a encore rempli aucun critere."""
    return all(criteres.get(critere) is None for critere in GOUTS + ["acces_handicap"])


def choisir_voyage(criteres: dict) -> dict | None:
    """Renvoie le voyage qui convient le mieux, ou None si aucun ne convient.

    Regle d'Eric, adoptee le 21/10 :
    - un Non du client est un vrai refus : les voyages qui ont ce critere sont exclus ;
    - acces_handicap a True est un besoin : les voyages non accessibles sont exclus ;
    - chaque Oui du client satisfait par le voyage vaut 1 point ;
    - a egalite, le premier voyage du fichier passe devant.
    Aucun voyage ne convient (option A, 21/10) si tous sont exclus, ou si le client
    a dit au moins un Oui et qu'aucun candidat n'en satisfait un seul.
    """
    # Un voyage est exclu s'il a un seul des criteres que le client refuse
    candidats = [
        voyage for voyage in VOYAGES
        if not any(criteres.get(gout) is False and voyage[gout] for gout in GOUTS)
    ]
    if criteres.get("acces_handicap") is True:
        candidats = [voyage for voyage in candidats if voyage["acces_handicap"]]
    # Liste vide : max planterait (ValueError), on s'arrete avant
    if not candidats:
        return None

    def score(voyage: dict) -> int:
        return sum(1 for gout in GOUTS if criteres.get(gout) is True and voyage[gout])

    # Etape 4b : max garde le premier des meilleurs, donc l'ordre du fichier
    meilleur = max(candidats, key=score)
    # Des Oui, mais aucun satisfait : 0 point n'est pas un choix (panne silencieuse du 21/10)
    if any(criteres.get(gout) is True for gout in GOUTS) and score(meilleur) == 0:
        return None
    return meilleur
