"""Cœur RDF : ontologies, écriture, sondage, veto-coût, chemin."""

from pathlib import Path

import pytest

from coeur.chemin import chercher_consensus
from coeur.graphe import ajouter_lien, ajouter_noeud, importer
from coeur.ontologie import declarer_ontologies_de_base
from coeur.requetes import executer
from coeur.regles import definir_regles
from coeur.session import ouvrir
from coeur.sondage import questions_ouvertes, repondre, sonder
from coeur.succes import definir_succes

RACINE = Path(__file__).resolve().parents[1]
FIXTURE = Path(__file__).resolve().parent / "fixtures" / "vacances.ttl"


def _session():
    session = ouvrir()
    declarer_ontologies_de_base(session)
    return session


def _noter(session, qui: str, option: str, note: float) -> None:
    question = sonder(session, qui, option, f"note de {qui} sur {option}")
    repondre(session, question, qui, option, note)


def test_classe_et_relation_non_declarees_sont_refusees():
    session = _session()
    with pytest.raises(ValueError, match="classe non déclarée"):
        ajouter_noeud(session, "domaine", "Hotel", "hotel")
    ajouter_noeud(session, "domaine", "Option", "a")
    ajouter_noeud(session, "domaine", "Option", "b")
    with pytest.raises(ValueError, match="relation non déclarée"):
        ajouter_lien(session, "domaine", "prefere", "a", "b")


def test_bretagne_n_est_pas_dans_le_coeur():
    for chemin in (RACINE / "coeur").rglob("*"):
        if chemin.suffix not in {".py", ".ttl", ".rq"}:
            continue
        texte = chemin.read_text(encoding="utf-8").lower()
        assert "bretagne" not in texte
        assert "hôtel" not in texte and "hotel" not in texte


def test_vacances_importees_par_la_porte_d_ecriture():
    session = _session()
    importer(session, FIXTURE)
    options = {ligne["option"] for ligne in executer(session, "options")}
    assert "bretagne" in options
    voisins = {ligne["voisin"] for ligne in executer(session, "voisins", noeud="voile")}
    assert "acces_mer" in voisins
    assert "nautique" in voisins


def test_sondage_ecrit_une_question_puis_une_reponse():
    session = _session()
    ajouter_noeud(session, "domaine", "Option", "repli")
    ajouter_noeud(session, "negociation", "Participant", "p1", {"label": "P1"})
    question = sonder(session, "p1", "repli", "que penses-tu du repli")
    assert questions_ouvertes(session) == [question]
    repondre(session, question, "p1", "repli", 2)
    assert questions_ouvertes(session) == []


def test_veto_coute_et_le_chemin_propose_une_concession():
    session = _session()
    for option in ("favori", "repli"):
        ajouter_noeud(session, "domaine", "Option", option)
    for personne in ("p1", "p2", "p3"):
        ajouter_noeud(session, "negociation", "Participant", personne)
        _noter(session, personne, "favori", 8)
        _noter(session, personne, "repli", 2)
    ajouter_noeud(session, "negociation", "Veto", "veto-p1-favori")
    ajouter_lien(session, "negociation", "auteur", "veto-p1-favori", "p1")
    ajouter_lien(session, "negociation", "cible", "veto-p1-favori", "favori")
    definir_regles(session, mode_veto="cout", veto_cout=100)
    definir_succes(session, critere="least_misery", tours_stables=3, max_tours=8)

    resultat = chercher_consensus(session)

    assert resultat["meilleur"] == "repli"
    assert resultat["tours"] == 3
    assert resultat["historique"][0]["direction"] == "conceder"
    assert resultat["historique"][0]["gain"] == pytest.approx(6)
    assert resultat["historique"][0]["scores"]["favori"]["least_misery"] == pytest.approx(-92)
    assert resultat["historique"][0]["scores"]["repli"]["least_misery"] == pytest.approx(2)
    options = {ligne["option"] for ligne in executer(session, "options")}
    assert "favori" in options
    assert any(ligne["pas"] == "conceder" and ligne["retenu"] in {"true", "True"} for ligne in resultat["chemins"])
