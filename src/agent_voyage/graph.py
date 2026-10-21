"""Le graphe de l'agent voyage, etape par etape comme le Grafcet."""

from typing import TypedDict

from langgraph.graph import END, START, StateGraph

from agent_voyage.extraction import extraire_criteres


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
    """Etape 1 : le modele extrait les criteres du message de l'utilisateur."""
    criteres = extraire_criteres(state["message_utilisateur"])
    return criteres.model_dump()


graph = (
    StateGraph(State)
    .add_node(extraire)
    .add_edge(START, "extraire")
    .add_edge("extraire", END)
    .compile(name="agent_voyage")
)
