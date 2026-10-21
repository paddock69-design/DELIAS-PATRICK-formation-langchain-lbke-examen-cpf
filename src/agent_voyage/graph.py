"""Le graphe de l'agent voyage, etape par etape comme le Grafcet."""

from typing import TypedDict

from langgraph.graph import END, START, StateGraph

from agent_voyage.choix import choisir_voyage
from agent_voyage.extraction import extraire_criteres
from agent_voyage.redaction import rediger_demande, rediger_proposition


class State(TypedDict):
    """Ce que l'agent garde d'un message a l'autre (cahier des charges)."""

    plage: bool | None
    montagne: bool | None
    ville: bool | None
    sport: bool | None
    detente: bool | None
    acces_handicap: bool | None
    message_utilisateur: str
    reponse_ia: str


def extraire(state: State) -> dict:
    """Etapes 1 et 2 : le modele extrait les criteres, seuls ceux cites changent."""
    criteres = extraire_criteres(state["message_utilisateur"])
    # None = le client n'en a rien dit : la case n'est pas renvoyee, l'ancienne valeur reste
    return criteres.model_dump(exclude_none=True)


def aiguiller(state: State) -> str:
    """Etape 3 : au moins un critere rempli ? choisir_voyage renvoie None sinon."""
    if choisir_voyage(state) is None:
        return "demander"
    return "proposer"


def demander(state: State) -> dict:
    """Etape 4a : aucun critere connu, le modele redige la demande de criteres."""
    return {"reponse_ia": rediger_demande(state["message_utilisateur"])}


def proposer(state: State) -> dict:
    """Etapes 4b et 5b : le voyage est choisi en Python, le modele redige la proposition."""
    voyage = choisir_voyage(state)
    # Le state entier est passe : la redaction y lit les envies et les refus de tous les tours
    return {"reponse_ia": rediger_proposition(state["message_utilisateur"], voyage, state)}


graph = (
    StateGraph(State)
    .add_node(extraire)
    .add_node(demander)
    .add_node(proposer)
    .add_edge(START, "extraire")
    .add_conditional_edges("extraire", aiguiller, ["demander", "proposer"])
    .add_edge("demander", END)
    .add_edge("proposer", END)
    .compile(name="agent_voyage")
)
