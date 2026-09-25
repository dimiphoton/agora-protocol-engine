"""Requêtes SPARQL nommées. Une requête = un fichier ``.rq``."""

from __future__ import annotations

from pathlib import Path

from rdflib import URIRef

from coeur.ns import uri_noeud
from coeur.session import Session, graphe_lecture

RACINE = Path(__file__).resolve().parent / "requetes"


def executer(session: Session, nom: str, **liens: str) -> list[dict]:
    """Exécute ``coeur/requetes/{nom}.rq``. ``liens`` lie des identifiants courts."""
    texte = (RACINE / f"{nom}.rq").read_text(encoding="utf-8")
    bindings = {}
    for cle, identifiant in liens.items():
        bindings[cle] = _resoudre(session, identifiant)
    lignes = []
    for ligne in graphe_lecture(session).query(texte, initBindings=bindings):
        lignes.append({str(cle): _valeur(ligne[cle]) for cle in ligne.labels})
    return lignes


def _resoudre(session: Session, identifiant: str) -> URIRef:
    if identifiant.startswith("http://") or identifiant.startswith("https://"):
        return URIRef(identifiant)
    for ontologie in session.ontologies:
        noeud = URIRef(uri_noeud(ontologie, identifiant))
        if any(session.faits.triples((noeud, None, None))):
            return noeud
    return URIRef(identifiant)


def _valeur(terme) -> str | None:
    if terme is None:
        return None
    texte = str(terme)
    if "/id/" in texte:
        return texte.split("/")[-1]
    return texte
