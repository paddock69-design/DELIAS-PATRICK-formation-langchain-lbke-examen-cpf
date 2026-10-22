"""Le graphe de l'agent voyage, etape par etape comme le Grafcet."""

from typing import TypedDict

from langgraph.graph import END, START, StateGraph

from agent_voyage.choix import choisir_voyage, aucun_critere, GOUTS
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
    criteres = extraire_criteres(state["message_utilisateur"],
                                 state.get("reponse_ia", ""))
    mise_a_jour = {}
    # Choix 1 du 22/10 : un non a la proposition efface les envies (True), les refus (False) restent
    if criteres.refuse_proposition:
        for gout in GOUTS:
            if state.get(gout) is True:
                mise_a_jour[gout] = None
    # None non renvoye = le client n'en a rien dit, l'ancienne valeur reste
    # refuse_proposition n'est pas un critere : il ne part pas dans le state
    mise_a_jour.update(criteres.model_dump(exclude_none=True, exclude={"refuse_proposition"}))
    return mise_a_jour


def aiguiller(state: State) -> str:
    """Etape 3 : aucun_critere est vrai on demande, sinon on choisit le voyage ou on signale qu'aucun ne convient."""
    if aucun_critere(state) is True:
        return "demander"
    if choisir_voyage(state) is None:
        return "aucun_voyage"
    return "proposer"


def demander(state: State) -> dict:
    """Etape 4a : aucun critere connu, le modele redige la demande de criteres."""
    return {"reponse_ia": rediger_demande(state["message_utilisateur"],
                                          state.get("reponse_ia", ""))}


def proposer(state: State) -> dict:
    """Etapes 4b et 5b : le voyage est choisi en Python, le modele redige la proposition."""
    voyage = choisir_voyage(state)
    # Le state entier est passe : la redaction y lit les envies de tous les tours
    return {"reponse_ia": rediger_proposition(state["message_utilisateur"], voyage, state)}


def aucun_voyage(state: State) -> dict:
    """Etape 4c : aucun voyage ne convient, message fixe ecrit en Python, sans le modele."""
    return {"reponse_ia": "Aucun voyage ne correspond à vos critères. Pouvez-vous préciser vos envies ?"}


graph = (
    StateGraph(State)
    .add_node(extraire)
    .add_node(demander)
    .add_node(proposer)
    .add_node(aucun_voyage)
    .add_edge(START, "extraire")
    .add_conditional_edges("extraire", aiguiller, ["demander", "proposer", "aucun_voyage"])
    .add_edge("demander", END)
    .add_edge("proposer", END)
    .add_edge("aucun_voyage", END)
    .compile(name="agent_voyage")
)
