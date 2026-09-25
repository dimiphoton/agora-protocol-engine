"""Le graphe grossit, et un chemin est retenu vers le consensus."""

from agora.core.chemins import essayer_chemins, lire_chemins, lire_direction
from agora.kr.charger import charger
from agora.kr.negociation import poser_negociation
from agora.scenarios import charger_scenario
from agora.simulateurs.boucle import jouer


def test_veto_teste_la_concession_et_lecrit_dans_le_graphe():
    scenario = charger_scenario("veto")
    graphe = charger(scenario)
    poser_negociation(scenario, graphe)
    avant = graphe.number_of_nodes()
    bilan = essayer_chemins(graphe, scenario["preferences"], numero=1, seed=0)
    assert graphe.number_of_nodes() > avant
    assert bilan["retenu"]["type"] == "conceder"
    assert bilan["retenu"]["gain"] > 0
    assert lire_direction(graphe, 1)["type"] == "conceder"
    chemins = lire_chemins(graphe)
    assert chemins
    assert any(chemin["retenu"] for chemin in chemins)
    assert any(chemin["type_chemin"] == "proposer" for chemin in chemins)


def test_jouer_enrichit_le_graphe_a_chaque_round():
    scenario = charger_scenario("vacances_3")
    resultat = jouer(scenario, scenario["profils"], seed=0, max_rounds=2)
    graphe = resultat["graphe"]
    chemins = lire_chemins(graphe)
    assert len({chemin["numero"] for chemin in chemins}) == 2
    assert resultat["historique"][0]["direction"]["type"]
    assert resultat["chemins"]
