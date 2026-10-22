"""Etape 1 du Grafcet : extraire les criteres du message de l'utilisateur."""

from pydantic import BaseModel

from agent_voyage.modele import modele


class CriteresExtraits(BaseModel):
    """Les 6 criteres du sujet, tels que le message les exprime, et le refus de la proposition."""

    plage: bool | None = None
    montagne: bool | None = None
    ville: bool | None = None
    sport: bool | None = None
    detente: bool | None = None
    acces_handicap: bool | None = None
    # Pas un critere : le client refuse-t-il le voyage que l'agence vient de proposer ?
    refuse_proposition: bool = False


PROMPT_EXTRACTION = """Tu analyses le message d'un client d'une agence de voyage.
Pour chacun des 6 criteres (plage, montagne, ville, sport, detente, acces_handicap), reponds :
- true si le client exprime un avis positif sur ce critere ;
- false seulement s'il refuse clairement ce critere ;
- null s'il n'en dit rien, ou s'il est indifferent.
Une destination ou le client dit vouloir aller implique les criteres qu'elle possede de facon evidente
(par exemple, des vacances dans une ville au bord de la mer impliquent plage et ville).
Un lieu cite sans envie d'y aller, par exemple dans une question de culture generale, n'exprime aucun avis : null.
Si un message de l'agence precede, il sert seulement a comprendre a quoi le client repond.
refuse_proposition : true si le client refuse le voyage que l'agence vient de lui proposer, sinon false.
Refuser un voyage n'est pas refuser ses criteres : un critere ne passe a false que si le client le refuse lui-meme.
N'invente jamais un avis que le client n'a pas exprime : dans le doute, null."""

extracteur = modele.with_structured_output(CriteresExtraits)


def extraire_criteres(message: str, reponse_precedente: str = "") -> CriteresExtraits:
    """Envoie la consigne, la derniere reponse de l'IA s'il y en a une, puis le message."""
    messages = [("system", PROMPT_EXTRACTION)]
    if reponse_precedente:
        messages.append(("ai", reponse_precedente))
    messages.append(("human", message))
    return extracteur.invoke(messages)
