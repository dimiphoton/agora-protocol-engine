"""Scénarios JSON : vacances, resto, weekend, cas limites."""

from agora.core.moteur import tourner
from agora.kr.charger import charger
from agora.kr.requetes import (
    combinaison_valide,
    dimensions,
    enumerer_candidats,
    valeurs,
)
from agora.scenarios import charger_scenario, preferences_figees
from agora.simulateurs.boucle import jouer

MOTS_VACANCES = {
    "bretagne",
    "mediterranee",
    "auvergne",
    "camping",
    "hotel",
    "voile",
    "velo",
    "festival",
    "vacances",
    "destination",
    "logement",
    "activite",
    "acces_mer",
}


def _produit(graphe) -> int:
    produit = 1
    for dimension in dimensions(graphe):
        produit *= len(valeurs(graphe, dimension))
    return produit


def _tourner_fige(nom: str) -> dict:
    scenario = charger_scenario(nom)
    return tourner(scenario, preferences_figees(scenario), seed=0)


def test_scenarios_passent_le_schema():
    noms = [
        "vacances_3",
        "vacances_large",
        "resto",
        "weekend",
        "unanimite",
        "conflit_total",
        "veto",
        "egalite",
        "prefs_manquantes",
    ]
    for nom in noms:
        scenario = charger_scenario(nom)
        graphe = charger(scenario)
        assert dimensions(graphe)
        assert enumerer_candidats(graphe, limite=1)


def test_preferences_figees_absentes_ou_presentes():
    assert preferences_figees(charger_scenario("vacances_3")) is None
    figées = preferences_figees(charger_scenario("veto"))
    assert figées is not None
    assert "favori" in figées["veto"]["p1"]


def test_vacances_3_voile_exige_la_mer():
    scenario = charger_scenario("vacances_3")
    graphe = charger(scenario)
    assert scenario["profils"]["alice"] == "cooperatif"
    assert scenario["profils"]["samir"] == "veto_prone"
    assert scenario["profils"]["lea"] == "incomplet"
    auvergne = next(noeud for noeud in scenario["noeuds"] if noeud["id"] == "auvergne")
    assert "montagne" in auvergne["traits"]
    assert "acces_mer" not in auvergne["traits"]
    assert not combinaison_valide(
        graphe,
        {"destination": "auvergne", "logement": "hotel", "activite": "voile"},
    )
    assert combinaison_valide(
        graphe,
        {"destination": "bretagne", "logement": "hotel", "activite": "voile"},
    )
    assert combinaison_valide(
        graphe,
        {
            "destination": "mediterranee",
            "logement": "camping",
            "activite": "voile",
        },
    )
    relations = {
        (rel["source"], rel["relation"], rel["cible"])
        for rel in scenario["relations"]
    }
    assert ("voile", "sous_type", "nautique") in relations
    assert ("voile", "requiert", "acces_mer") in relations
    assert ("festival", "implique", "budget_eleve") in relations
    assert len(enumerer_candidats(graphe)) <= 2000


def test_resto_et_weekend_ne_sont_pas_des_vacances():
    vacances = charger_scenario("vacances_3")
    ids_vacances = {noeud["id"] for noeud in vacances["noeuds"]}
    for nom in ("resto", "weekend"):
        scenario = charger_scenario(nom)
        assert scenario["domaine"] != "vacances"
        ids = {noeud["id"] for noeud in scenario["noeuds"]}
        assert ids.isdisjoint(ids_vacances)
        assert ids.isdisjoint(MOTS_VACANCES)
        graphe = charger(scenario)
        assert len(enumerer_candidats(graphe)) < _produit(graphe)
        assert len(enumerer_candidats(graphe)) > 0
        resultat = tourner(scenario, preferences_figees(scenario), seed=0)
        assert resultat["meilleur"] is not None
        assert resultat["meilleur"]["id"] == resultat["classement"][0]["id"]
        for mot in MOTS_VACANCES:
            assert mot not in resultat["meilleur"]["id"]


def test_veto_candidat_classe_mais_perd():
    scenario = charger_scenario("veto")
    prefs = preferences_figees(scenario)
    resultat = tourner(scenario, prefs, seed=0)
    vetoes = [cible for cibles in prefs["veto"].values() for cible in cibles]
    touches = [
        candidat
        for candidat in resultat["classement"]
        if any(valeur in vetoes for valeur in candidat["choix"].values())
    ]
    assert touches
    assert resultat["meilleur"]["id"] not in {candidat["id"] for candidat in touches}
    assert touches[0]["penalite"] >= 100
    assert resultat["meilleur"]["id"] == "option=repli"


def test_unanimite_gagnant_clair():
    resultat = _tourner_fige("unanimite")
    meilleur = resultat["meilleur"]
    assert meilleur["least_misery"] >= 8
    assert meilleur["least_misery"] > resultat["classement"][1]["least_misery"]
    assert meilleur["id"] == "a=a0|b=b0"


def test_egalite_departagee_par_la_moyenne():
    resultat = _tourner_fige("egalite")
    premier, second = resultat["classement"][0], resultat["classement"][1]
    assert premier["least_misery"] == second["least_misery"]
    assert premier["moyenne"] > second["moyenne"]
    assert premier["id"] == "option=haute"
    assert second["id"] == "option=basse"


def test_conflit_total_least_misery_mediocre():
    resultat = _tourner_fige("conflit_total")
    meilleur = resultat["meilleur"]
    assert meilleur is not None
    assert meilleur["penalite"] == 0
    assert -5 < meilleur["least_misery"] < 5
    assert meilleur["id"] == "x=x0|y=y1"


def test_prefs_manquantes_laissent_un_gagnant():
    scenario = charger_scenario("prefs_manquantes")
    resultat = tourner(scenario, preferences_figees(scenario), seed=0)
    assert resultat["meilleur"] is not None
    assert resultat["metriques"]["taux_manquant"] > 0.5
    assert resultat["meilleur"]["id"] == "a=a0|b=b1"


def test_vacances_large_depasse_2000_et_joue():
    scenario = charger_scenario("vacances_large")
    graphe = charger(scenario)
    assert len(scenario["participants"]) == 8
    assert len(enumerer_candidats(graphe, limite=2001)) > 2000
    profils = set(scenario["profils"].values())
    assert {"cooperatif", "veto_prone", "incomplet", "bruite"} <= profils
    resultat = jouer(scenario, scenario["profils"], seed=0, max_rounds=2)
    assert resultat["mode"] == "genetique"
    assert len(resultat["historique"]) == 2
    assert resultat["meilleur"] is not None
    assert resultat["accord"]["meilleur_id"] == resultat["meilleur"]["id"]
