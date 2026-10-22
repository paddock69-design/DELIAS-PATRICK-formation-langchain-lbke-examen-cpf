"""Tests des etapes 3 et 4b : choisir le voyage en Python, sans appeler le modele."""

from agent_voyage.choix import aucun_critere, choisir_voyage


def test_montpellier_donne_palavas() -> None:
    voyage = choisir_voyage({"plage": True, "ville": True})
    assert voyage["nom"] == "Palavas de paillotes en paillotes"


def test_montagne_en_fauteuil_donne_chamonix_fondue() -> None:
    voyage = choisir_voyage({"montagne": True, "acces_handicap": True})
    assert voyage["nom"] == "5 étoiles à Chamonix option fondue"


def test_tous_les_voyages_exclus_donne_none() -> None:
    assert choisir_voyage({"montagne": False, "detente": False}) is None


def test_oui_jamais_satisfait_donne_none() -> None:
    assert choisir_voyage({"plage": False, "ville": True}) is None


def test_que_des_refus_donne_le_premier_non_exclu() -> None:
    voyage = choisir_voyage({"plage": False})
    assert voyage["nom"] == "Randonnée camping en Lozère"


def test_aucun_critere() -> None:
    assert aucun_critere({}) is True
    assert aucun_critere({"plage": False}) is False
