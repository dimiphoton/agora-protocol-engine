"""Carte de l'espace : domaine valide, falaise, Pareto, frontière acceptable."""

import json
from pathlib import Path

from agora.core.frontieres import PLAFOND_PAYSAGE, analyser_frontieres

FIXTURE = Path(__file__).resolve().parent / "fixtures" / "mini_vacances.json"


def _mini() -> dict:
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def _scenario_veto() -> dict:
    from agora.scenarios import charger_scenario

    return charger_scenario("veto")


def test_veto_reste_dans_le_domaine_et_tombe_sous_le_seuil():
    scenario = _scenario_veto()
    carte = analyser_frontieres(scenario, scenario["preferences"], seuil=0.0)
    assert carte["complet"] is True
    assert carte["espace"]["produit"] == 2
    assert carte["espace"]["valides"] == 2
    assert carte["falaise_veto"]["n"] == 1
    assert carte["acceptable"]["n"] == 1

    par_id = {point["id"]: point for point in carte["points"]}
    favori = next(point for point in carte["points"] if "favori" in point["id"])
    repli = next(point for point in carte["points"] if "repli" in point["id"])
    assert favori["falaise"] is True
    assert favori["acceptable"] is False
    assert favori["least_misery"] == -92
    assert repli["acceptable"] is True
    assert repli["frontiere"] is True
    # Les deux restent Pareto : le veto n'efface pas le point, il l'enfonce
    # sur une seule coordonnée.
    assert favori["pareto"] is True
    assert repli["pareto"] is True
    assert favori["id"] in par_id


def test_graphe_retire_des_combinaisons_du_produit():
    scenario = _mini()
    prefs = {"notes": {"p1": {"hotel": 4}, "p2": {"hotel": 1}}, "veto": {}}
    carte = analyser_frontieres(scenario, prefs, seuil=0.0)
    assert carte["espace"]["produit"] == 12
    assert carte["espace"]["valides"] < 12
    assert carte["espace"]["valides"] >= 1
    assert carte["frontiere_dure"]
    assert carte["coupe"]["axe_x"]
    assert len(carte["coupe"]["cellules"]) >= 1


def test_plafond_annonce_sans_dessiner_un_faux_paysage(monkeypatch):
    scenario = _scenario_veto()
    monkeypatch.setattr(
        "agora.core.frontieres.taille_produit",
        lambda graphe: PLAFOND_PAYSAGE + 1,
    )
    carte = analyser_frontieres(scenario, scenario["preferences"])
    assert carte["complet"] is False
    assert "points" not in carte
    assert carte["espace"]["valides"] is None
