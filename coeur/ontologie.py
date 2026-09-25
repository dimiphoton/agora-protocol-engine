"""Déclaration des ontologies. Un fichier Turtle par ontologie."""

from __future__ import annotations

from pathlib import Path

from rdflib import Graph

from coeur.session import Session

RACINE = Path(__file__).resolve().parent
ONTOLOGIES = RACINE / "ontologies"


def declarer_ontologie(session: Session, nom: str, fichier: str | Path | None = None) -> Graph:
    """Charge une ontologie nommée. Refuse un second chargement du même nom."""
    if nom in session.ontologies:
        raise ValueError(f"ontologie déjà déclarée : {nom}")
    chemin = Path(fichier) if fichier else ONTOLOGIES / f"{nom}.ttl"
    if not chemin.is_file():
        raise FileNotFoundError(f"ontologie introuvable : {chemin}")
    graphe = Graph()
    graphe.parse(chemin, format="turtle")
    session.ontologies[nom] = graphe
    return graphe


def declarer_ontologies_de_base(session: Session) -> None:
    """Charge ``domaine`` et ``negociation``."""
    declarer_ontologie(session, "domaine")
    declarer_ontologie(session, "negociation")
