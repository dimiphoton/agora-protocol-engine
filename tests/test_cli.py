"""CLI : scénarios, veto, version git. N'importe pas Streamlit."""

import json

from agora.cli import main
from agora.scenarios import charger_scenario, preferences_figees
from agora.version import version_git


def test_version_git_renvoie_une_chaine():
    version = version_git()
    assert isinstance(version, str)
    assert version.strip()


def test_scenarios_contient_resto_et_weekend(capsys):
    assert main(["scenarios"]) == 0
    data = json.loads(capsys.readouterr().out)
    ids = [item["id"] for item in data]
    assert "resto" in ids
    assert "weekend" in ids


def test_run_veto_le_candidat_vetoe_n_est_pas_le_meilleur(tmp_path, capsys):
    scenario = charger_scenario("veto")
    prefs = preferences_figees(scenario)
    assert prefs is not None
    chemin = tmp_path / "prefs.json"
    chemin.write_text(json.dumps(prefs), encoding="utf-8")

    assert main(["run", "veto", "--prefs", str(chemin)]) == 0
    data = json.loads(capsys.readouterr().out)
    _assert_veto_perd(data, prefs)

    assert main(["run", "veto"]) == 0
    figee = json.loads(capsys.readouterr().out)
    _assert_veto_perd(figee, prefs)


def test_run_vacances_3_simuler(capsys):
    assert main(["run", "vacances_3", "--simuler", "--seed", "0"]) == 0
    data = json.loads(capsys.readouterr().out)
    assert data["meilleur"]["id"]
    assert data["historique"]
    assert "graphe" not in data
    assert data["version"]
    assert data["mode"] in {"exhaustif", "genetique"}


def test_scenario_inconnu(capsys):
    assert main(["run", "introuvable"]) == 1
    capture = capsys.readouterr()
    assert capture.out == ""
    assert "introuvable" in capture.err.lower()


def _assert_veto_perd(data: dict, prefs: dict) -> None:
    assert "meilleur" in data
    meilleur = data["meilleur"]
    for champ in ("id", "least_misery", "moyenne", "penalite", "dispersion"):
        assert champ in meilleur
    assert "historique" in data
    assert "accord" in data
    assert "mode" in data
    assert data["version"]
    vetoes = [cible for cibles in prefs["veto"].values() for cible in cibles]
    assert vetoes
    assert not any(valeur in vetoes for valeur in meilleur["choix"].values())
    assert "graphe" not in data
