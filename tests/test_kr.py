"""Requêtes sur le graphe : requiert, héritage, implique.

Les libellés du domaine sont dans tests/fixtures/mini_vacances.json.
"""

import json
from pathlib import Path

from agora.core.evaluation import evaluer_candidat
from agora.core.moteur import tourner
from agora.kr.charger import charger
from agora.kr.requetes import (
    combinaison_valide,
    dimensions,
    enumerer_candidats,
    etendre_preferences,
    valeurs,
)

FIXTURE = Path(__file__).parent / "fixtures" / "mini_vacances.json"


def _graphe():
    return charger(FIXTURE)


def _choix(destination: str, logement: str, activite: str) -> dict[str, str]:
    return {
        "destination": destination,
        "logement": logement,
        "activite": activite,
    }


def test_fixture_trois_dimensions_deux_par_deux_par_trois():
    graphe = _graphe()
    assert dimensions(graphe) == ["destination", "logement", "activite"]
    tailles = [len(valeurs(graphe, dim)) for dim in dimensions(graphe)]
    assert tailles == [2, 2, 3]

    premiers = enumerer_candidats(graphe)
    seconds = enumerer_candidats(graphe)
    assert [candidat["id"] for candidat in premiers] == [
        candidat["id"] for candidat in seconds
    ]
    assert premiers[0]["id"] == (
        "destination=bretagne|logement=hotel|activite=voile"
    )
    assert premiers[0]["choix"]["destination"] == "bretagne"


def test_voile_requiert_acces_mer():
    graphe = _graphe()
    assert not combinaison_valide(graphe, _choix("auvergne", "hotel", "voile"))
    assert combinaison_valide(graphe, _choix("bretagne", "hotel", "voile"))

    retenus = enumerer_candidats(graphe)
    assert not any(
        candidat["choix"]["activite"] == "voile"
        and candidat["choix"]["destination"] == "auvergne"
        for candidat in retenus
    )
    assert any(
        candidat["choix"]["activite"] == "voile"
        and candidat["choix"]["destination"] == "bretagne"
        for candidat in retenus
    )


def test_incompatible_si_trait_present():
    graphe = _graphe()
    refuse = _choix("auvergne", "camping", "randonnee")
    accepte = _choix("bretagne", "camping", "randonnee")
    assert not combinaison_valide(graphe, refuse)
    assert combinaison_valide(graphe, accepte)


def test_preference_parent_nautique_heritee_par_voile():
    graphe = _graphe()
    etendues = etendre_preferences(
        graphe,
        {"notes": {"p1": {"nautique": 6}}, "veto": {}},
    )
    assert etendues["notes"]["p1"]["voile"] == 6
    assert etendues["notes"]["p1"]["nautique"] == 6
    assert "festival" not in etendues["notes"]["p1"]

    propre = etendre_preferences(
        graphe,
        {"notes": {"p1": {"nautique": 6, "voile": -1}}, "veto": {}},
    )
    assert propre["notes"]["p1"]["voile"] == -1


def test_implique_budget_eleve_applique_a_festival_sans_note_propre():
    graphe = _graphe()
    etendues = etendre_preferences(
        graphe,
        {"notes": {"p1": {"budget_eleve": -4}}, "veto": {}},
    )
    assert etendues["notes"]["p1"]["festival"] == -4

    avec_propre = etendre_preferences(
        graphe,
        {"notes": {"p1": {"budget_eleve": -4, "festival": 3}}, "veto": {}},
    )
    assert avec_propre["notes"]["p1"]["festival"] == 3


def test_note_sur_un_trait_portee_par_le_noeud():
    graphe = _graphe()
    etendues = etendre_preferences(
        graphe,
        {"notes": {"p1": {"acces_mer": 5}}, "veto": {}},
    )
    assert etendues["notes"]["p1"]["bretagne"] == 5
    assert "auvergne" not in etendues["notes"]["p1"]


def test_veto_sur_classe_parente_penalise_sans_retirer():
    graphe = _graphe()
    choix = _choix("bretagne", "hotel", "voile")
    candidat = next(
        item for item in enumerer_candidats(graphe) if item["choix"] == choix
    )
    evaluation = evaluer_candidat(
        candidat,
        ["p1"],
        {"p1": {"voile": 2}},
        {"p1": ["nautique"]},
        graphe,
    )
    assert evaluation["detail"]["p1"]["nb_veto"] == 1
    assert evaluation["detail"]["p1"]["satisfaction_ajustee"] == -98


def test_requiert_satisfait_par_une_relation_fournit():
    scenario = {
        "id": "fourniture",
        "domaine": "abstrait",
        "dimensions": ["gauche", "droite"],
        "noeuds": [
            {"id": "a", "type": "gauche", "label": "A", "traits": []},
            {"id": "b", "type": "droite", "label": "B", "traits": []},
            {"id": "c", "type": "droite", "label": "C", "traits": []},
            {
                "id": "besoin",
                "type": "concept",
                "label": "Besoin",
                "traits": [],
            },
        ],
        "relations": [
            {"source": "a", "relation": "requiert", "cible": "besoin"},
            {"source": "b", "relation": "fournit", "cible": "besoin"},
        ],
        "participants": [{"id": "p", "label": "P"}],
    }
    graphe = charger(scenario)
    assert combinaison_valide(graphe, {"gauche": "a", "droite": "b"})
    assert not combinaison_valide(graphe, {"gauche": "a", "droite": "c"})


def test_tourner_garde_le_veto_et_filtre_les_invalides():
    scenario = json.loads(FIXTURE.read_text(encoding="utf-8"))
    preferences = {
        "notes": {
            "p1": {"nautique": 8, "bretagne": 4},
            "p2": {"festival": -2},
        },
        "veto": {"p1": ["camping"]},
    }
    resultat = tourner(scenario, preferences, seed=0)
    assert resultat["historique"] == []
    assert resultat["meilleur"]["id"] == resultat["classement"][0]["id"]
    assert any(
        candidat["choix"]["logement"] == "camping"
        for candidat in resultat["classement"]
    )
    assert all(
        not (
            candidat["choix"]["activite"] == "voile"
            and candidat["choix"]["destination"] == "auvergne"
        )
        for candidat in resultat["classement"]
    )
    for cle in ("least_misery", "moyenne", "penalite", "dispersion"):
        assert resultat["metriques"][cle] == resultat["meilleur"][cle]
    assert "H_round" in resultat["metriques"]
    json.dumps(resultat)
