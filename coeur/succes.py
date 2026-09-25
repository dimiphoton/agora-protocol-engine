"""Critère de succès, écrit sur le même réglage que les règles."""

from __future__ import annotations

from coeur.criteres import CRITERES
from coeur.graphe import poser_attribut
from coeur.requetes import executer
from coeur.session import Session


def definir_succes(
    session: Session,
    critere: str = "least_misery",
    tours_stables: int = 3,
    max_tours: int = 8,
    seuil: float | None = None,
) -> None:
    """Choisit le critère nommé et la condition d'arrêt."""
    if critere not in CRITERES:
        raise ValueError(f"critère inconnu : {critere}")
    if not executer(session, "reglage"):
        raise ValueError("definir_regles d'abord")
    poser_attribut(session, "reglage", "critere", critere)
    poser_attribut(session, "reglage", "toursStables", int(tours_stables))
    poser_attribut(session, "reglage", "maxTours", int(max_tours))
    if seuil is not None:
        poser_attribut(session, "reglage", "seuil", float(seuil))


def lire_succes(session: Session) -> dict:
    """Relit le critère et l'arrêt par SPARQL."""
    lignes = executer(session, "reglage")
    if not lignes or not lignes[0].get("critere"):
        raise ValueError("aucun critère de succès défini")
    premiere = lignes[0]
    seuil = premiere.get("seuil")
    return {
        "critere": premiere["critere"],
        "tours_stables": int(float(premiere["toursStables"])),
        "max_tours": int(float(premiere["maxTours"])),
        "seuil": None if seuil is None else float(seuil),
    }
