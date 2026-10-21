"""Etape 1 du Grafcet : extraire les criteres du message de l'utilisateur."""

from pydantic import BaseModel

from agent_voyage.modele import modele


class CriteresExtraits(BaseModel):
    """Les 6 criteres du sujet, tels que le message les exprime."""

    plage: bool | None = None
    montagne: bool | None = None
    ville: bool | None = None
    sport: bool | None = None
    detente: bool | None = None
    acces_handicap: bool | None = None


PROMPT_EXTRACTION = """Tu analyses le message d'un client d'une agence de voyage.
Pour chacun des 6 criteres (plage, montagne, ville, sport, detente, acces_handicap), reponds :
- true si le client exprime un avis positif sur ce critere ;
- false s'il exprime un avis negatif ou indifferent sur ce critere ;
- null s'il ne dit rien sur ce critere.
Une destination ou le client dit vouloir aller implique les criteres qu'elle possede de facon evidente
(par exemple, des vacances dans une ville au bord de la mer impliquent plage et ville).
Un lieu cite sans envie d'y aller, par exemple dans une question de culture generale, n'exprime aucun avis : null.
N'invente jamais un avis que le client n'a pas exprime : dans le doute, null."""

extracteur = modele.with_structured_output(CriteresExtraits)


def extraire_criteres(message: str) -> CriteresExtraits:
    """Envoie la consigne et le message au modele, renvoie les 6 criteres."""
    return extracteur.invoke([("system", PROMPT_EXTRACTION), ("human", message)])
