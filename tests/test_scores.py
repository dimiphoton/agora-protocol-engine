"""Contrat de scores : exemple chiffré, notes manquantes, départages."""

import math

import pytest

from agora.core.evaluation import classer, evaluer_candidat
from agora.core.scores import (
    agreger,
    ajuster_veto,
    entropie_round,
    fitness_key,
    satisfaction_individu,
)


def test_exemple_chiffre_a_devant_b_et_b_present():
    agregat_a = agreger([8, -2], [0, 0])
    assert agregat_a["least_misery"] == -2
    assert agregat_a["moyenne"] == 3
    assert agregat_a["penalite"] == 0
    assert agregat_a["dispersion"] == 5

    s1_b = ajuster_veto(2, 1, 100)
    assert s1_b == -98
    agregat_b = agreger([s1_b, 6], [100, 0])
    assert agregat_b["least_misery"] == -98
    assert agregat_b["moyenne"] == -46
    assert agregat_b["penalite"] == 100
    assert agregat_b["dispersion"] == 52

    # B est donné en premier : le tri doit quand même placer A devant.
    candidats = [
        {"id": "B", "choix": {"opt": "b"}},
        {"id": "A", "choix": {"opt": "a"}},
    ]
    preferences = {"p1": {"a": 8, "b": 2}, "p2": {"a": -2, "b": 6}}
    veto = {"p1": ["b"]}
    classement = classer(candidats, ["p1", "p2"], preferences, veto)

    assert [candidat["id"] for candidat in classement] == ["A", "B"]
    a = classement[0]
    b = classement[1]
    assert a["least_misery"] == -2
    assert a["moyenne"] == 3
    assert b["detail"]["p1"]["satisfaction_ajustee"] == -98
    assert b["least_misery"] == -98
    assert b["moyenne"] == -46
    assert b["penalite"] == 100


def test_prefs_manquantes_moyenne_sur_les_notes_connues():
    assert satisfaction_individu([8, -2]) == 3
    assert satisfaction_individu([]) == 0

    candidat = {"id": "c", "choix": {"d1": "a", "d2": "b", "d3": "c"}}
    une_note = evaluer_candidat(candidat, ["p1"], {"p1": {"a": 9}}, {})
    assert une_note["detail"]["p1"]["notes"] == [9]
    assert une_note["detail"]["p1"]["satisfaction"] == 9

    aucune = evaluer_candidat(candidat, ["p1"], {"p1": {}}, {})
    assert aucune["detail"]["p1"]["satisfaction"] == 0
    assert aucune["least_misery"] == 0
    assert aucune["moyenne"] == 0


def test_egalite_least_misery_departagee_par_la_moyenne():
    candidats = [
        {"id": "basse", "choix": {"opt": "basse"}},
        {"id": "haute", "choix": {"opt": "haute"}},
    ]
    # Même plancher (0), moyenne 0 contre 3.
    preferences = {
        "p1": {"basse": 0, "haute": 0},
        "p2": {"basse": 0, "haute": 6},
    }
    classement = classer(candidats, ["p1", "p2"], preferences, {})
    assert classement[0]["id"] == "haute"
    assert classement[0]["least_misery"] == classement[1]["least_misery"] == 0
    assert classement[0]["moyenne"] > classement[1]["moyenne"]


def test_dispersion_puis_penalite_departagent():
    serree = agreger([0, 3, 3], [0, 0, 0])
    etalee = agreger([0, 0, 6], [0, 0, 0])
    assert serree["least_misery"] == etalee["least_misery"] == 0
    assert serree["moyenne"] == etalee["moyenne"] == 2
    assert serree["dispersion"] < etalee["dispersion"]
    assert fitness_key(serree) < fitness_key(etalee)

    sans_cout = {
        "least_misery": 1.0,
        "moyenne": 1.0,
        "dispersion": 0.0,
        "penalite": 0.0,
    }
    avec_cout = {**sans_cout, "penalite": 100.0}
    assert fitness_key(sans_cout) < fitness_key(avec_cout)


def test_entropie_uniforme_puis_taux_manquant():
    entropie = entropie_round([0.0, 0.0], 0.5)
    assert entropie["H_classement"] == pytest.approx(math.log(2))
    assert entropie["taux_manquant"] == 0.5
    assert entropie["H_round"] == pytest.approx(math.log(2) + 0.5)
