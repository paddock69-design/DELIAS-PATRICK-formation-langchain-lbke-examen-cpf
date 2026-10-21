"""Etapes 4a et 5b du Grafcet : rediger la reponse au client."""

from agent_voyage.modele import modele

CRITERES = ["plage", "montagne", "ville", "sport", "detente", "acces_handicap"]

PROMPT_PROPOSITION = """Tu es le conseiller d'une agence de voyage. Tu reponds au client en un seul court message.
Le voyage a proposer est deja choisi : {nom}.
Ce que l'on sait de ce voyage, et rien d'autre : {atouts}.
Regles :
- propose ce voyage et aucun autre ;
- n'utilise que les informations ci-dessus : n'invente ni duree, ni prix, ni programme, ni hebergement, ni activite ;
- 2 ou 3 phrases, sans titre ni liste ;
- termine en invitant le client a preciser ses envies parmi : plage, montagne, ville, sport, detente, acces handicap."""

PROMPT_ENVIES = """
Le client veut : {envies}. Ce voyage le lui offre : commence par la, c'est la raison de la proposition."""

PROMPT_REFUS = """
Le client a refuse : {refus}. Ce voyage le comporte : dis-le franchement en une phrase, et ne le presente jamais comme un atout."""


def rediger_proposition(message: str, voyage: dict, criteres: dict) -> str:
    """Le voyage est deja choisi en Python : le modele redige seulement la proposition."""
    # Le code donne les faits : les criteres que possede le voyage, lus dans le fichier
    atouts = ", ".join(critere for critere in CRITERES if voyage[critere])
    # Envies et refus viennent du state, donc de tous les tours, pas du seul dernier message
    envies = [critere for critere in CRITERES if criteres.get(critere) is True and voyage[critere]]
    refus = [critere for critere in CRITERES if criteres.get(critere) is False and voyage[critere]]
    consigne = PROMPT_PROPOSITION.format(nom=voyage["nom"], atouts=atouts)
    # Chaque consigne n'est donnee que si elle s'applique : sinon le modele invente
    if envies:
        consigne += PROMPT_ENVIES.format(envies=", ".join(envies))
    if refus:
        consigne += PROMPT_REFUS.format(refus=", ".join(refus))
    return modele.invoke([("system", consigne), ("human", message)]).content
