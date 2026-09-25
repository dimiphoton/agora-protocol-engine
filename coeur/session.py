"""Une session : les ontologies déclarées et les faits."""

from __future__ import annotations

from dataclasses import dataclass, field

from rdflib import Graph


@dataclass
class Session:
    """État du cœur. Les faits et les ontologies sont des graphes RDF."""

    faits: Graph = field(default_factory=Graph)
    ontologies: dict[str, Graph] = field(default_factory=dict)
    tour: int = 0


def ouvrir() -> Session:
    """Session vide. Aucune ontologie n'est chargée."""
    return Session()


def graphe_lecture(session: Session) -> Graph:
    """Union des ontologies et des faits, pour les requêtes SPARQL."""
    lecture = Graph()
    for graphe in session.ontologies.values():
        lecture += graphe
    lecture += session.faits
    return lecture
