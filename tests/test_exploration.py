"""Exhaustif sous le seuil, génétique appelée directement au-dessus."""

import json

from agora.core.evaluation import classer, evaluer_candidat
from agora.core.exploration import SEUIL_EXHAUSTIF, explorer, genetique
from agora.core.moteur import tourner
from agora.core.scores import fitness_key
from agora.kr.charger import charger
from agora.kr.requetes import combinaison_valide, enumerer_candidats


def _scenario_petit() -> dict:
    noeuds = []
    for dimension, nombre in (("a", 2), ("b", 2)):
        for index in range(nombre):
            noeuds.append(
                {
                    "id": f"{dimension}{index}",
                    "type": dimension,
                    "label": f"{dimension}{index}",
                    "traits": [],
                }
            )
    return {
        "id": "petit",
        "domaine": "abstrait",
        "dimensions": ["a", "b"],
        "noeuds": noeuds,
        "relations": [],
        "participants": [
            {"id": "p1", "label": "P1"},
            {"id": "p2", "label": "P2"},
        ],
    }


def _scenario_cinquante() -> dict:
    """6 × 5 × 2 bruts, un requiert ramène le valide à 50."""
    noeuds = []
    for index in range(6):
        noeuds.append(
            {
                "id": f"x{index}",
                "type": "x",
                "label": f"X{index}",
                "traits": ["marque"] if index >= 2 else [],
            }
        )
    for index in range(5):
        noeuds.append(
            {
                "id": f"y{index}",
                "type": "y",
                "label": f"Y{index}",
                "traits": [],
            }
        )
    for index in range(2):
        noeuds.append(
            {
                "id": f"z{index}",
                "type": "z",
                "label": f"Z{index}",
                "traits": [],
            }
        )
    noeuds.append(
        {"id": "marque", "type": "trait", "label": "Marque", "traits": []}
    )
    return {
        "id": "espace50",
        "domaine": "abstrait",
        "dimensions": ["x", "y", "z"],
        "noeuds": noeuds,
        "relations": [
            {"source": "z1", "relation": "requiert", "cible": "marque"},
        ],
        "participants": [{"id": "p", "label": "P"}],
    }


def _evaluer_score(candidat: dict) -> dict:
    choix = candidat["choix"]
    score = (
        int(choix["x"][1:])
        + int(choix["y"][1:])
        + 10 * int(choix["z"][1:])
    )
    return {
        "least_misery": float(score),
        "moyenne": float(score),
        "penalite": 0.0,
        "dispersion": 0.0,
    }


def test_seuil_exhaustif_est_celui_du_contrat():
    assert SEUIL_EXHAUSTIF == 2000


def test_petit_espace_exhaustif_meilleur_egal_au_classement():
    graphe = charger(_scenario_petit())
    participants = ["p1", "p2"]
    preferences = {
        "p1": {"a0": 5, "b0": 1, "a1": -8},
        "p2": {"a0": -1, "a1": 2, "b1": 4},
    }
    veto = {"p1": ["a1"]}
    candidats = enumerer_candidats(graphe)
    assert len(candidats) <= SEUIL_EXHAUSTIF

    classement = classer(candidats, participants, preferences, veto, graphe)

    def evaluer(candidat: dict) -> dict:
        return evaluer_candidat(
            candidat, participants, preferences, veto, graphe
        )

    resultat = explorer(graphe, evaluer, seed=0)
    assert resultat["mode"] == "exhaustif"
    assert len(resultat["classement"]) == len(candidats)
    assert resultat["meilleur"]["id"] == classement[0]["id"]
    assert any(
        candidat["choix"]["a"] == "a1"
        for candidat in resultat["classement"]
    )


def test_explorer_choisit_exhaustif_sous_le_seuil():
    graphe = charger(_scenario_cinquante())
    candidats = enumerer_candidats(graphe)
    assert len(candidats) == 50
    assert len(candidats) <= SEUIL_EXHAUSTIF

    resultat = explorer(graphe, _evaluer_score, seed=0)
    assert resultat["mode"] == "exhaustif"
    assert len(resultat["classement"]) == 50
    def cle(candidat: dict) -> tuple:
        return fitness_key(_evaluer_score(candidat))

    meilleur = min(candidats, key=cle)
    assert resultat["meilleur"]["id"] == meilleur["id"]


def test_genetique_trouve_le_meilleur_exhaustif():
    graphe = charger(_scenario_cinquante())
    candidats = enumerer_candidats(graphe)
    meilleur = min(
        ({**candidat, **_evaluer_score(candidat)} for candidat in candidats),
        key=fitness_key,
    )
    trouve = genetique(graphe, _evaluer_score, seed=0)
    assert trouve is not None
    assert combinaison_valide(graphe, trouve["choix"])
    assert fitness_key(trouve) == fitness_key(meilleur)


def test_tourner_un_round_jsonable():
    scenario = _scenario_petit()
    preferences = {
        "notes": {
            "p1": {"a0": 5, "b0": 1, "a1": -8},
            "p2": {"a0": -1, "a1": 2, "b1": 4},
        },
        "veto": {"p1": ["a1"]},
    }
    resultat = tourner(scenario, preferences, seed=0)
    assert resultat["historique"] == []
    assert resultat["meilleur"]["id"] == resultat["classement"][0]["id"]
    for cle in ("least_misery", "moyenne", "penalite", "dispersion"):
        assert resultat["metriques"][cle] == resultat["meilleur"][cle]
    assert resultat["metriques"]["taux_manquant"] == 0.25
    json.dumps(resultat)
