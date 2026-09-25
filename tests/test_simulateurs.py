"""Profils de vote et boucle multi-rounds."""

import copy

from agora.kr.negociation import lire_accord, lire_rounds
from agora.scenarios import charger_scenario
from agora.simulateurs.boucle import PROFILS, jouer, participants_du_round
from agora.simulateurs.bruite import voter as voter_bruite
from agora.simulateurs.cooperatif import voter as voter_cooperatif
from agora.simulateurs.incomplet import voter as voter_incomplet
from agora.simulateurs.veto_prone import voter as voter_veto


def _mini(gouts: dict) -> dict:
    return {
        "id": "mini_profil",
        "domaine": "abstrait",
        "dimensions": ["item"],
        "noeuds": [
            {"id": "x", "type": "item", "label": "X", "traits": []},
            {"id": "y", "type": "item", "label": "Y", "traits": []},
            {"id": "z", "type": "item", "label": "Z", "traits": []},
        ],
        "relations": [],
        "participants": [{"id": "p", "label": "P"}],
        "gouts": {"p": gouts},
    }


def test_profils_bornent_les_notes():
    scenario = charger_scenario("vacances_3")
    personne = {"id": "p", "label": "P"}
    borne = _mini({"x": 10, "y": -10, "z": 0})
    for seed in range(12):
        for nom, voter in PROFILS.items():
            for participant in scenario["participants"]:
                vote = voter(participant, scenario, seed)
                assert vote["notes"], nom
                for note in vote["notes"].values():
                    assert -10 <= note <= 10, nom
            vote_borne = {
                "cooperatif": voter_cooperatif,
                "veto_prone": voter_veto,
                "incomplet": voter_incomplet,
                "bruite": voter_bruite,
            }[nom](personne, borne, seed)
            for note in vote_borne["notes"].values():
                assert -10 <= note <= 10, nom


def test_veto_prone_veto_si_gout_sous_moins_cinq():
    scenario = _mini({"x": -4, "y": -6, "z": 3})
    vote = voter_veto({"id": "p", "label": "P"}, scenario, seed=0)
    assert "y" in vote["veto"]
    assert "x" not in vote["veto"]
    assert vote["notes"]["x"] == -6
    assert vote["notes"]["y"] == -8
    assert vote["notes"]["z"] == 3

    vacances = charger_scenario("vacances_3")
    samir = voter_veto({"id": "samir", "label": "Samir"}, vacances, seed=0)
    assert samir["veto"]
    assert any(vacances["gouts"]["samir"][cible] < -5 for cible in samir["veto"])


def test_incomplet_a_des_trous():
    scenario = charger_scenario("vacances_3")
    from agora.simulateurs.commun import ids_domaine

    domaine = ids_domaine(scenario)
    vote = voter_incomplet({"id": "lea", "label": "Léa"}, scenario, seed=0)
    absents = len(domaine) - len(vote["notes"])
    assert absents == round(0.4 * len(domaine))
    assert absents > 0
    assert set(vote["notes"]) < set(domaine)


def test_bruite_ecarte_la_note_de_base():
    from agora.simulateurs.commun import notes_de_base

    scenario = charger_scenario("vacances_3")
    participant = {"id": "alice", "label": "Alice"}
    base = notes_de_base(participant, scenario)
    ecarte = False
    for seed in range(5):
        vote = voter_bruite(participant, scenario, seed)
        assert set(vote["notes"]) == set(base)
        assert vote["veto"] == []
        if any(vote["notes"][cle] != base[cle] for cle in base):
            ecarte = True
    assert ecarte


def test_cooperatif_prefs_completes_sans_veto():
    from agora.simulateurs.commun import ids_domaine

    scenario = charger_scenario("vacances_3")
    vote = voter_cooperatif({"id": "alice", "label": "Alice"}, scenario, seed=0)
    assert vote["veto"] == []
    assert set(vote["notes"]) == set(ids_domaine(scenario))


def test_round_robin_ne_prend_qu_une_partie():
    ids = ["a", "b", "c"]
    assert participants_du_round(ids, 1) == ["a"]
    assert participants_du_round(ids, 2) == ["b"]
    assert participants_du_round(ids, 3) == ["c"]
    assert participants_du_round(ids, 4) == ["a"]
    gros = [f"p{i}" for i in range(8)]
    bloc = participants_du_round(gros, 1)
    assert len(bloc) == 4
    assert set(bloc).isdisjoint(participants_du_round(gros, 2))
    assert participants_du_round(["seul"], 1) == ["seul"]


def test_jouer_vacances_3_rounds_entropie_et_accord():
    scenario = charger_scenario("vacances_3")
    resultat = jouer(scenario, scenario["profils"], seed=0)
    historique = resultat["historique"]
    assert 1 <= len(historique) <= 8
    for ligne in historique:
        assert isinstance(ligne["entropie"], float)
        assert "taux_manquant" in ligne
        assert ligne["notes_recues"] >= 1
    if len(historique) < 8:
        derniers = [ligne["meilleur_id"] for ligne in historique[-3:]]
        assert derniers[0] == derniers[1] == derniers[2]
    for index in range(len(historique) - 3):
        trio = [historique[index + decalage]["meilleur_id"] for decalage in range(3)]
        assert not (trio[0] == trio[1] == trio[2])

    graphe = resultat["graphe"]
    rounds = lire_rounds(graphe)
    accord = lire_accord(graphe)
    assert [ligne["numero"] for ligne in rounds] == [
        ligne["round"] for ligne in historique
    ]
    assert [ligne["meilleur_id"] for ligne in rounds] == [
        ligne["meilleur_id"] for ligne in historique
    ]
    assert accord is not None
    assert accord == resultat["accord"]
    assert accord["meilleur_id"] == resultat["meilleur"]["id"]
    assert len(accord["clauses"]) == len(scenario["dimensions"])
    assert all(" = " in clause["texte"] for clause in accord["clauses"])
    labels_classes = {
        data.get("label")
        for _noeud, data in graphe.nodes(data=True)
        if data.get("type") == "classe"
    }
    assert {"proposition", "round", "veto", "clause", "accord"} <= labels_classes
    assert any(
        data.get("type") == "participant" for _noeud, data in graphe.nodes(data=True)
    )
    assert any(data.get("type") == "veto" for _noeud, data in graphe.nodes(data=True))
    assert resultat["classement"][0]["id"] == resultat["meilleur"]["id"]
    assert resultat["metriques"]["least_misery"] == resultat["meilleur"]["least_misery"]


def test_arret_apres_trois_rounds_identiques():
    scenario = copy.deepcopy(charger_scenario("unanimite"))
    scenario["gout_groupe"] = {"a0": 10, "a1": -8, "b0": 10, "b1": -8}
    profils = {participant["id"]: "cooperatif" for participant in scenario["participants"]}
    resultat = jouer(scenario, profils, seed=0, max_rounds=8)
    assert len(resultat["historique"]) == 3
    assert len({ligne["meilleur_id"] for ligne in resultat["historique"]}) == 1

    court = jouer(scenario, profils, seed=0, max_rounds=2)
    assert len(court["historique"]) == 2
